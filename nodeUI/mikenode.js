var cursorX = 0;
var cursorY = 0;

var isPressing = false;
var nodeTree = {
	nodes: []
};

var postRequest = function() {
	$.post(
		"/api/nodes",
		JSON.stringify(nodeTree),
		function() {
			console.log("successful post request");
		},
		"json"
	);
};

var body = document.querySelector("body");
// Listening for the mouse and touch events
body.addEventListener("mousedown", pressingDown, false);
body.addEventListener("mouseup", notPressingDown, false);
body.addEventListener("mouseleave", notPressingDown, false);

function pressingDown(e) {
	isPressing = true;
}

function notPressingDown(e) {
	isPressing = false;
}

window.onload = init;
function init() {
	if (window.Event) {
		document.captureEvents(Event.MOUSEMOVE);
	}
	document.onmousemove = getCursorXY;
}

function getCursorXY(e) {
	cursorX = window.Event
		? e.pageX
		: event.clientX +
		  (document.documentElement.scrollLeft
				? document.documentElement.scrollLeft
				: document.body.scrollLeft);
	cursorY = window.Event
		? e.pageY
		: event.clientY +
		  (document.documentElement.scrollTop
				? document.documentElement.scrollTop
				: document.body.scrollTop);
}
// master variables
var styles = "";
var nodes = [];

// update

var boxCenterXOffset = 10;
var boxCenterYOffset = 10;

setInterval(function() {
	update();
}, 30);

var numOn = 0;
var nodes = [[]];
var inHand = false;
var list = 0;

var c = document.getElementById("canvas");

c.width = window.innerWidth;
c.height = window.innerHeight;
var ctx = c.getContext("2d");
$(document).ready(function() {
	//add input first

	$("body").on("mousedown", ".clicker", function() {
		if (
			$(this)
				.parent()
				.attr("class") == "inputContainer"
		) {
			popLoop(nodes, $(this).attr("id"));
			postRequest();
		} else if (
			$(this)
				.parent()
				.attr("class") == "outputContainer"
		) {
			nodes[list].push($(this).attr("id"));

			inHand = true;
		}
	});
	$("body").on("mouseup", ".clicker", function() {
		if (
			$(this)
				.parent()
				.attr("class") == "inputContainer"
		) {
			if (inHand) {
				if (
					nodes[list][0].substring(36, 39) ==
						$(this)
							.attr("id")
							.substring(36, 39) &&
					!searchForInput(nodes, $(this).attr("id"))
				) {
					nodes[list].push($(this).attr("id"));
					inHand = false;
				} else {
					inHand = false;
					nodes[list].pop();
				}
			}
			if (nodes[list].length == 2) {
				findNodeTreeSpot(
					$("#" + nodes[list][1])
						.parent()
						.parent()
						.parent()
						.attr("id")
				).inputs[nodes[list][1].substring(39)] = {
					id: $("#" + nodes[list][0])
						.parent()
						.parent()
						.parent()
						.attr("id"),
					name: nodes[list][0].substring(39)
				};

				postRequest();

				nodes[list + 1] = [];
				list++;
				firsttime = true;
				onOut = false;
			}
		} else {
		}
	});
});

function update() {
	if (!isPressing) {
		if (inHand) {
			inHand = false;
			nodes[list].pop();
		}
	}

	c.width = window.innerWidth;
	c.height = window.innerHeight;

	ctx.strokeStyle = "#2DBC4E";
	ctx.lineWidth = 5;
	for (let i = 0; i < nodes.length; i++) {
		if (nodes[i].length == 2) {
			//math to find points
			var x1 = $("#" + nodes[i][0]).offset().left + boxCenterXOffset;
			var x2 = $("#" + nodes[i][1]).offset().left + boxCenterXOffset;
			var y1 = $("#" + nodes[i][0]).offset().top + boxCenterYOffset;
			var y2 = $("#" + nodes[i][1]).offset().top + boxCenterYOffset;

			ctx.beginPath();
			ctx.moveTo(x1, y1);
			ctx.bezierCurveTo((x1 + x2) / 2, y1, (x1 + x2) / 2, y2, x2, y2);
			ctx.stroke();
		}
	}
	if (inHand) {
		$(".input").css("cursor", "crosshair");

		var x1 = $("#" + nodes[list][0]).offset().left + boxCenterXOffset;
		var x2 = cursorX;
		var y1 = $("#" + nodes[list][0]).offset().top + boxCenterYOffset;
		var y2 = cursorY;

		ctx.beginPath();
		ctx.moveTo(x1, y1);
		ctx.bezierCurveTo((x1 + x2) / 2, y1, (x1 + x2) / 2, y2, x2, y2);
		ctx.stroke();
	} else {
		$(".input").css("cursor", "not-allowed");
	}
}
// class declarations
const Node = function(id, uuid, settings, inputs, outputs, name) {
	this.uuid = uuid;
	this.name = name;

	this.settings = settings;
	this.inputs = inputs;
	this.outputs = outputs;
	this.id = id;
	this.create = function() {
		$("#container").prepend(
			'<div class="node" id="' +
				this.uuid +
				'">' +
				"<h1>" +
				this.name +
				"</h1>" +
				'<div class="ioContainer">' +
				'<div class="inputContainer">' +
				inputLoop(this.inputs, this.uuid) +
				"</div>" +
				'<div class="outputContainer">' +
				outputLoop(this.outputs, this.uuid) +
				"</div>" +
				"</div>" +
				settingsLoop(this.settings, uuid) +
				"</div>"
		);
		$("#" + this.uuid).draggable({
			cancel: ".clicker, input, select"
		});
		settingsGo(this.settings);
	};
};

// ------------------------------------- settings land ------------------------------------------------------

const intInput = function(name) {
	this.value = null;
	this.id = "";
	this.create = function(uuid) {
		this.id = uuid;
		return (
			'<input type="number" class="numInput int setting" oninput="" id="' +
			uuid +
			name +
			'">' +
			"</input>"
		);
	};
	this.go = function() {
		let id = this.id;

		$("#" + this.id + name)
			.on("keyup", function(e) {
				if (e.which === 46) return false;
			})
			.on("input", function() {
				var self = this;
				setTimeout(function() {
					if (self.value.indexOf(".") != -1)
						self.value = parseInt(self.value, 10);
				}, 0);
			});
		$("#" + this.id + name).on("input", function() {
			findNodeTreeSpot(
				$(this)
					.parent()
					.parent()
					.attr("id")
			).settings[name] = parseFloat($(this).val());
			postRequest();
		});
	};
};
const decInput = function(name) {
	this.value = null;
	this.id = "";
	this.create = function(uuid) {
		this.id = uuid;
		return (
			'<input type="number" class="numInput setting" oninput="" id="' +
			uuid +
			name +
			'">' +
			"</input>"
		);
	};
	this.go = function() {
		let id = this.id;

		
		$("#" + this.id + name).on("input", function() {
			findNodeTreeSpot(
				$(this)
					.parent()
					.parent()
					.attr("id")
			).settings[name] = parseFloat($(this).val());
			postRequest();
		});
	};
};

const strInput = function(name) {
	this.value = null;
	this.id = "";
	this.create = function(uuid) {
		this.id = uuid;
		return (
			'<input class="strInput setting" oninput="" id="' +
			uuid +
			name +
			'">' +
			"</input>"
		);
	};
	this.go = function() {
		let id = this.id;
		$("#" + this.id + name).on("input", function() {
			findNodeTreeSpot(
				$(this)
					.parent()
					.parent()
					.attr("id")
			).settings[name] = $(this).val();
			postRequest();
		});
	};
};

const booleanInput = function(name) {
	this.value = null;
	this.id = "";
	this.create = function(uuid) {
		this.id = uuid;
		return (
			'<label class="switch">' +
			'<input type="checkbox" id="' +
			uuid +
			name +
			'">' +
			'<span class="slidey round"></span>' +
			"</label>"
		);
	};
	this.go = function() {
		let id = this.id;
		$("#" + this.id + name).on("change", function() {
			if (this.checked) {
				findNodeTreeSpot(
					$(this)
						.parent()
						.parent()
						.parent()
						.attr("id")
				).settings[name] = true;
			} else {
				findNodeTreeSpot(
					$(this)
						.parent()
						.parent()
						.parent()
						.attr("id")
				).settings[name] = false;
			}
			postRequest();
		});
	};
};

const range = function(min, max, name) {
	this.min = min;
	this.max = max;
	this.minVal = min;
	this.maxVal = max;
	var slider = null;
	this.id = "";
	this.create = function(uuid) {
		this.id = uuid;
		return (
			'<div class="setting slider" id="' +
			uuid +
			name +
			'"></div><div id="' +
			uuid +
			name +
			'out1"class="setting sliderOut">' +
			this.minVal +
			'</div><div id="' +
			uuid +
			name +
			'out2"class="setting sliderOut2">' +
			this.maxVal +
			"</div>"
		);
	};
	this.go = function() {
		$("#" + this.id + name).slider({
			range: true,
			min: this.min,
			max: this.max,
			values: [this.min, this.max],
			slide: function(event, ui) {
				this.minVal = ui.values[0];
				this.maxVal = ui.values[1];

				findNodeTreeSpot(
					$(this)
						.parent()
						.parent()
						.attr("id")
				).settings[name] = { min: parseFloat(this.minVal), max: parseFloat(this.maxVal) };

				$("#" + this.id + "out1").text(this.minVal);

				$("#" + this.id + "out2").text(this.maxVal);
				//tofix too many post requests probably
				postRequest();
			}
		});
	};
};

const slide = function(min, max, name) {
	this.min = min;
	this.max = max;
	this.val = (max + min) / 2;
	var slider = null;
	this.id = "";
	this.create = function(uuid) {
		this.id = uuid;
		return (
			'<div class="setting slider" id="' +
			uuid +
			name +
			'"></div><div id="' +
			uuid +
			name +
			'out"class="setting sliderOut">' +
			this.val +
			"</div>"
		);
	};
	this.go = function() {
		$("#" + this.id + name).slider({
			range: false,
			min: this.min,
			max: this.max,
			value: this.val,
			slide: function(event, ui) {
				this.val = ui.value;

				findNodeTreeSpot(
					$(this)
						.parent()
						.parent()
						.attr("id")
				).settings[name] = parseFloat(this.val);

				$("#" + this.id + "out").text(this.val);

				//tofix too many post requests probably
				postRequest();
			}
		});
	};
};

const box = function(options, name) {
	this.options = options;
	this.value = options[0];
	this.id = "";
	let loopy = function() {
		let going = "";
		for (let i = 0; i < options.length; i++) {
			going += "<option value=" + options[i] + ">" + options[i] + "</option>";
		}
		return going;
	};
	this.create = function(uuid) {
		this.id = uuid;
		return (
			'<select class="setting dropdown" id="' +
			uuid +
			name +
			'">' +
			loopy() +
			"</select>"
		);
	};
	this.go = function() {
		$("#" + this.id + name).on("change", function() {
			findNodeTreeSpot(
				$(this)
					.parent()
					.parent()
					.attr("id")
			).settings[name] = $(this).val();
			postRequest();
		});
	};
};

var findNodeTreeSpot = function(finder) {
	for (let i = 0; i < nodeTree.nodes.length; i++) {
		if (nodeTree.nodes[i].id == finder) {
			return nodeTree.nodes[i];
		}
	}
	throw "error!";
};

var inputLoop = function(array, uuid) {
	let arr = [];
	if (array && array.length) {
		for (let i = 0; i < array.length - 1; i++) {
			arr +=
				'<div class="clicker input" id="' +
				uuid +
				array[i] +
				array[array.length - 1][i].replace(/\s+/g, "") +
				'">' +
				"</div>" +
				"<div class='inputDesc'>" +
				array[array.length - 1][i] +
				"</div>";
		}
		return arr;
	} else {
		return "";
	}
};
var outputLoop = function(array, uuid) {
	let arr = [];
	if (array && array.length) {
		for (let i = 0; i < array.length - 1; i++) {
			arr +=
				'<div class="clicker output" id="' +
				uuid +
				array[i] +
				array[array.length - 1][i].replace(/\s+/g, "") +
				'">' +
				"</div>" +
				"<div class='outputDesc'>" +
				array[array.length - 1][i] +
				"</div>";
		}
		return arr;
	} else {
		return "";
	}
};
var settingsLoop = function(settings, uuid) {
	if (settings && settings.length) {
		let arr = [];
		for (let i = 0; i < settings.length; i++) {
			arr += '<div class="itemContainer">';
			arr +=
				'<div class="setting settingName">' +
				"<h3>" +
				settings[i][0] +
				"</h3>" +
				"</div>";
			arr += settings[i][1].create(uuid);
			arr += "</div>";
		}
		return arr;
	} else {
		return "";
	}
};
var searchForInput = function(array, name) {
	for (let i = 0; i < array.length; i++) {
		if (array[i][1] == name) {
			return true;
		}
	}
	return false;
};

settingsGo = function(settings) {
	if (settings && settings.length) {
		for (let i = 0; i < settings.length; i++) {
			settings[i][1].go();
		}
	}
};
$("#" + nodes[list][1])
	.parent()
	.parent()
	.parent()
	.attr("id");

var popLoop = function(loop, id) {
	for (let i = 0; i < loop.length; i++) {
		if (loop[i].indexOf(id) != -1) {
			delete findNodeTreeSpot(
				$("#" + loop[i][1])
					.parent()
					.parent()
					.parent()
					.attr("id")
					.substring(0, 36)
			).inputs[loop[i][1].substring(39)];

			loop.splice(i, 1);
			list--;
		}
	}
};

//tofix

function uuid(a) {
	return a
		? (a ^ ((Math.random() * 16) >> (a / 4))).toString(16)
		: ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, uuid);
}

var nodeCount = 0;
//json functions
const functions = function(jsonData) {
	this.rawArr = [];
	this.inputs = [];
	this.inputsCount = -1;
	this.outputsCount = -1;
	this.settingsCount = -1;
	this.settings = [];
	this.outputs = [];
	this.name = [];
	for (let i = 0; i < jsonData.funcs.length; i++) {
		let array = jsonData.funcs[i];
		this.rawArr.push([
			array.name,
			array.type,
			array.settings,
			array.inputs,
			array.outputs,
			uuid()
		]);
		this.name.push(array.name);
	}
	for (let i = 0; i < this.rawArr.length; i++) {
		this.outputs.push([]);
		this.outputsCount++;
		let numinn = 0;
		let numoutt = 0;
		this.inputs.push([]);
		this.inputsCount++;
		for (x in this.rawArr[i][3]) {
			this.inputs[this.inputsCount].push(this.rawArr[i][3][x].type);
			numinn++;
		}
		if (numinn != 0) {
			this.inputs[this.inputsCount].push(Object.keys(this.rawArr[i][3]));
		}
		for (x in this.rawArr[i][4]) {
			this.outputs[this.outputsCount].push(this.rawArr[i][4][x].type);
			numoutt++;
		}
		if (numoutt != 0) {
			this.outputs[this.outputsCount].push(Object.keys(this.rawArr[i][4]));
		}
	}

	for (let i = 0; i < this.rawArr.length; i++) {
		let j = 0;
		this.settings.push([]);
		this.settingsCount++;
		for (x in this.rawArr[i][2]) {
			let nam = Object.keys(this.rawArr[i][2]);

			switch (this.rawArr[i][2][x].type) {
				case "dec":
					this.settings[this.settingsCount].push([x, new decInput(nam[j])]);
					break;
				case "int":
					this.settings[this.settingsCount].push([x, new intInput(nam[j])]);
					break;
				case "string":
					this.settings[this.settingsCount].push([x, new strInput(nam[j])]);
					break;
				case "boolean":
					this.settings[this.settingsCount].push([x, new booleanInput(nam[j])]);
					break;
				case "slide":
					this.settings[this.settingsCount].push([
						x,
						new slide(
							this.rawArr[i][2][x].params.min,
							this.rawArr[i][2][x].params.max,
							nam[j]
						)
					]);
					break;
				case "range":
					this.settings[this.settingsCount].push([
						x,
						new range(
							this.rawArr[i][2][x].params.min,
							this.rawArr[i][2][x].params.max,
							nam[j]
						)
					]);
					break;
				case "box":
					this.settings[this.settingsCount].push([
						x,
						new box(this.rawArr[i][2][x].params.options, nam[j])
					]);
					break;
			}
			j++;
		}
	}

	this.findType = function(name, parentType, inputs) {
		if (inputs) {
			for (let i = 0; i < this.rawArr.length; i++) {
				if (this.rawArr[i][1] == parentType) {
					return this.rawArr[i][3][name].type;
				}
			}
		} else {
			for (let i = 0; i < this.rawArr.length; i++) {
				if (this.rawArr[i][1] == parentType) {
					return this.rawArr[i][4][name].type;
				}
			}
		}
		return "fail";
	};

	//returns setting type of imported nodetree obj (since nodetree doesnt give setting)
	this.findSettingType = function(name, parentType) {
		for (let i = 0; i < this.rawArr.length; i++) {
			if (this.rawArr[i][1] == parentType) {

				return this.rawArr[i][2][name].type;
			}
		}
	};

	this.recreate = function(type, uuid) {
		for (let i = 0; i < this.rawArr.length; i++) {
			if (this.rawArr[i][1] === type) {
				functionNode = new Node(
					"node" + nodeCount,
					uuid,
					this.settings[i],
					this.inputs[i],
					this.outputs[i],
					this.name[i]
				);
				nodeTree.nodes.push({
					type: type,
					id: uuid,
					settings: {},
					inputs: {}
				});
				functionNode.create();
			}
		}
	};

	var go = function(type, arr, set, inp, out, name) {
		for (let i = 0; i < arr.length; i++) {
			if (arr[i][1] === type) {
				let uuidIn = uuid();
				functionNode = new Node(
					"node" + nodeCount,
					uuidIn,
					set[i],
					inp[i],
					out[i],
					name[i]
				);
				nodeTree.nodes.push({
					type: type,
					id: uuidIn,
					settings: {},
					inputs: {}
				});
				functionNode.create();
			}
		}
		postRequest();
	};

	this.ui = function() {
		for (let i = 0; i < this.rawArr.length; i++) {
			$("#menu-container").append(
				'<div class="menu-button" id="' +
					this.rawArr[i][5] +
					'">' +
					this.rawArr[i][0] +
					"</div>"
			);
			let gType = this.rawArr[i][1];
			let gArray = this.rawArr;
			let gSettings = this.settings;
			let gInputs = this.inputs;
			let gOutputs = this.outputs;
			let gName = this.name;
			$("#" + this.rawArr[i][5]).on("click", function() {
				go(gType, gArray, gSettings, gInputs, gOutputs, gName);
			});
		}
	};
};
const importNodeTree = function(nodetree, functions) {
	this.findOutputType = function(id) {
		for (let i = 0; i < nodetree.nodes.length; i++) {
			if (nodetree.nodes[i].id == id) {
				return nodetree.nodes[i].type;
			}
		}
	};

	this.go = function() {
		for (let i = 0; i < nodetree.nodes.length; i++) {
			//nodes
			functions.recreate(nodetree.nodes[i].type, nodetree.nodes[i].id);
			//inputs
			if (Object.keys(nodetree.nodes[i].inputs).length != 0) {
				for (x in nodetree.nodes[i].inputs) {
					nodes[list].push(
						nodetree.nodes[i].inputs[x].id +
							functions.findType(
								nodetree.nodes[i].inputs[x].name,
								this.findOutputType(nodetree.nodes[i].inputs[x].id, false)
							) +
							nodetree.nodes[i].inputs[x].name
					);

					nodes[list].push(
						nodetree.nodes[i].id +
							functions.findType(x, nodetree.nodes[i].type, true) +
							x
					);

					nodes[list + 1] = [];
					list++;
					firsttime = true;
					onOut = false;
				}
			}

			//settings

			for (x in nodetree.nodes[i].settings) {
				switch (functions.findSettingType(x, nodetree.nodes[i].type)) {
					case "dec":
						$("#" + nodetree.nodes[i].id + x).val(
							nodetree.nodes[i].settings[x]
						);
						break;
					case "int":
						$("#" + nodetree.nodes[i].id + x).val(
							nodetree.nodes[i].settings[x]
						);
						break;
					case "string":
						$("#" + nodetree.nodes[i].id + x).val(
							nodetree.nodes[i].settings[x]
						);
						break;
					case "boolean":
						if (nodetree.nodes[i].settings[x] == "true") {
							$("#" + nodetree.nodes[i].id + x).prop("checked", true);
						} else {
							$("#" + nodetree.nodes[i].id + x).prop("checked", false);
						}
						break;
					case "slide":
						$("#" + nodetree.nodes[i].id + x).slider(
							"value",
							nodetree.nodes[i].settings[x]
						);
						$("#" + nodetree.nodes[i].id + x + "out").text(
							nodetree.nodes[i].settings[x]
						);

						break;
					case "range":
						$("#" + nodetree.nodes[i].id + x).slider("values", [
							nodetree.nodes[i].settings[x].min,
							nodetree.nodes[i].settings[x].max
						]);
						$("#" + nodetree.nodes[i].id + x + "out1").text(
							nodetree.nodes[i].settings[x].min
						);

						$("#" + nodetree.nodes[i].id + x + "out2").text(
							nodetree.nodes[i].settings[x].max
						);
						// $('#' + nodetree.nodes[i].id + x).maxVal(nodetree.nodes[i].settings[x].max);
						break;
					case "box":
						$("#" + nodetree.nodes[i].id + x).val(
							nodetree.nodes[i].settings[x]
						);
						break;
				}
				// console.log('#' + nodetree.nodes[i].id + x);
			}
		}
		nodeTree.nodes = nodetree.nodes;
		postRequest();
	};
};
// const node = function(id, uuid, settings, inputs, outputs, name) {
