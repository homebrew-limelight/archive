(function (global) {
    function Frontend(container, api_endpoint) {
        LiteGraph.debug = true;

        if (container.constructor == String) {
            container = document.querySelector(container);
        }

        this.container = container;
        this.api_endpoint = api_endpoint || "";

        this.editor = Frontend.createEditor(container);

        this.server_load();
        this.server_restore();
        this.initUI();
    }

    Frontend.createEditor = function (container) {
        var editor = new LiteGraph.Editor(container, { skip_everything: true });
        editor.graphcanvas.show_info = false;
        $(window).resize(() => editor.graphcanvas.resize());

        return editor;
    }

    Frontend.prototype.initUI = function () {
        this.editor.addToolsButton(
            "save_button",
            "Save",
            "",
            this.server_save.bind(this),
            ".tools-left"
        );
        this.editor.addToolsButton(
            "load_button",
            "Load",
            "",
            this.server_restore.bind(this),
            ".tools-left"
        );
        this.editor.addToolsButton(
            "run_button",
            "Run Once",
            "",
            this.server_run.bind(this),
            ".tools-right"
        );
        this.editor.addToolsButton(
            "clear_button",
            "Clear",
            "",
            this.editor.graph.clear,
            ".footer .tools-left"
        );
        this.editor.addToolsButton(
            "demo_button",
            "Load Demo",
            "",
            () => {
                this.restore(JSON.parse(
                    '{"last_node_id":7,"last_link_id":8,"nodes":[{"id":1,"type":"demo/five","pos":[20,130],"size":{"0":140,"1":26},"flags":{},"mode":0,"outputs":[{"name":"five","type":"number","links":[0,4]}],"properties":{}},{"id":5,"type":"demo/print","pos":[590,180],"size":{"0":140,"1":26},"flags":{},"mode":0,"inputs":[{"name":"val","type":"number","link":5}],"properties":{"val":0}},{"id":6,"type":"demo/print","pos":[570,70],"size":{"0":140,"1":26},"flags":{},"mode":0,"inputs":[{"name":"val","type":"number","link":7}],"properties":{"val":0}},{"id":7,"type":"demo/multiply","pos":[380,190],"size":{"0":140,"1":46},"flags":{},"mode":0,"inputs":[{"name":"num1","type":"number","link":4},{"name":"num2","type":"number","link":3}],"outputs":[{"name":"product","type":"number","links":[5]}],"properties":{"num1":0,"num2":0}},{"id":2,"type":"demo/sum","pos":[260,50],"size":{"0":210,"1":78},"flags":{},"mode":0,"inputs":[{"name":"num1","type":"number","link":0},{"name":"num2","type":"number","link":null}],"outputs":[{"name":"out","type":"number","links":[7]}],"properties":{"num1":0,"num2":50}},{"id":4,"type":"demo/sum","pos":[80,220],"size":{"0":210,"1":102},"flags":{},"mode":0,"inputs":[{"name":"num1","type":"number","link":null},{"name":"num2","type":"number","link":null}],"outputs":[{"name":"out","type":"number","links":[3]}],"properties":{"num1":10,"num2":90}}],"links":[[0,1,0,2,0,"number"],[3,4,0,7,1,"number"],[4,1,0,7,0,"number"],[5,7,0,5,0,"number"],[7,2,0,6,0,"number"]],"groups":[],"config":{"align_to_grid":true},"version":0.4}'
                ))
            },
            ".footer .tools-right"
        )
    };

    Frontend.prototype.save = function () {
        return JSON.stringify(this.editor.graph.serialize());
    };

    Frontend.prototype.restore = function (state) {
        this.editor.graph.configure(state);
        this.editor.graph.config.align_to_grid = true;
    };

    // API

    Frontend.prototype.send = function (url, data, method, callback) {
        url = this.api_endpoint + url;

        if (method == 0) {
            data = null;
        } else {
            if (!data || data.constructor != String) {
                data = JSON.stringify(data || {});
            }
        }

        var params = {
            type: (method == 0) ? "GET" : "POST",
            url: url,
            dataType: 'json',
            async: true,
            data: data,
            success: callback || (nul => { }),
            // Todo: add error notification
            contentType: 'application/json'
        };

        return $.ajax(params);
    };

    Frontend.prototype.server_restore = function () {
        return this.send("/restore", null, 0, this.restore.bind(this));
    };

    Frontend.prototype.server_save = function () {
        return this.send("/save", this.editor.graph.serialize(), 1, (data) => console.log(data));
    };

    // Load Function definitions
    Frontend.prototype.server_load = function () {
        callback = data => {
            console.log("Loading functions: " + data);

            data.funcs.forEach(func => {
                Frontend.makeNodeType(func);
            });
        };

        return this.send("/load", null, 0, callback);
    };

    Frontend.prototype.server_update = function () {
        return this.send("/update_manager", null, 1, null);
    };

    Frontend.prototype.server_info = function () {
        return this.send("/info", null, 0, data => console.log(data));
    };

    Frontend.prototype.server_run = function () {
        return this.send("/saveAndRun", this.editor.graph.serialize(), 1, null);
    };


    // The NodeTemplate class is the parent class of all custom Nodes
    // It should not be used; use makeNodeType instead
    function NodeTemplate() {
        // Constructor intended to run after init of all IO and widgets
        this.all_widgets = (this.widgets || []).slice(0); // clone array
        this.size = this.computeSize();
    }

    // Use this.addThisInput instead of this.addInput in order to create corresponding widget
    NodeTemplate.prototype.addThisInput = function (name, type, params) {
        params = params || {};
        switch (type) {
            case "number":
                params.default_ = params.default_ || 0;
                params.min = params.min || 0;
                params.max = params.max || 100;
                this.addThisWidget(name, "number", "slider", params);
                break;
            case "bool":
                params.default_ = params.default_ || false;
                this.addThisWidget(name, "bool", "toggle", params);
                break;
            case "string":
                params.default_ = params.default_ || "";
                this.addThisWidget(name, "string", "string", params);
                break;
            default:
                params.default_ = params.default_ || 0;
                this.addInput(name, type, params.default_);
                break;
        }
    };

    NodeTemplate.prototype.addThisWidget = function (name, type, widget, params) {
        var callback = (v) => { this.properties[name] = v; this.onExecute() };

        this.addProperty(name, params.default_, type, params);
        this.addInput(name, type, params.default_);
        this.addWidget(widget, name, params.default_, callback, params);
    };

    NodeTemplate.prototype.getInput = function (name) {
        var data = this.getInputData(name);
        return (data === null) ? this.properties[name] : data;
    };

    NodeTemplate.prototype.onConnectionsChange = function (type) { // several unused params
        // Only need to update widgets if input changed
        if (!(type == LiteGraph.INPUT)) {
            return;
        }

        // Get an array of all the names of connected inputs
        var connected = this.inputs
            .filter(element => element.link !== null)
            .map(element => element.name);

        // Only show those widgets what have unconnected inputs
        this.widgets = this.all_widgets
            .filter(widget => connected.indexOf(widget.name) == -1);

        this.size = this.computeSize(); // This will override any user resizings

        this.onExecute();
    };

    NodeTemplate.prototype.onConfigure = function (info) {
        this.all_widgets.forEach(widget => {
            widget.value = this.properties[widget.name];
        });
    }

    NodeTemplate.prototype.onExecute = function () { }

    // IO is type object: {name, type, params}
    // params is type object: {default_, ...(extra widget options)}
    // Note: no onExecute method
    Frontend.makeNodeType = function (func) {
        function NewNode() {
            func.inputs.forEach(element => {
                this.addThisInput(element.name, element.type, element.params);
            });

            func.outputs.forEach(element => {
                this.addOutput(element.name, element.type, null); // Default output?
            });

            NodeTemplate.call(this); // super().__init__()
        }

        func.inputs.params = func.inputs.params || {};

        // JS inheritance is wack
        NewNode.prototype = Object.create(NodeTemplate.prototype);
        NewNode.prototype.constructor = NewNode;

        NewNode.title = func.name.split("/")[1];
        LiteGraph.registerNodeType(func.name, NewNode);
    };

    global.Frontend = Frontend;
})(this);
