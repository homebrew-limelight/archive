BASIC_SUM = """{
    "last_node_id": 3,
    "last_link_id": 2,
    "nodes": [
        {
            "id": 3,
            "type": "Sum",
            "pos": [
                390,
                110
            ],
            "size": {
                "0": 140,
                "1": 46
            },
            "flags": {},
            "mode": 0,
            "inputs": [
                {
                    "name": "num1",
                    "type": "number",
                    "link": 0
                },
                {
                    "name": "num2",
                    "type": "number",
                    "link": 1
                }
            ],
            "outputs": [
                {
                    "name": "out",
                    "type": "number",
                    "links": null
                }
            ],
            "properties": {}
        },
        {
            "id": 1,
            "type": "Five",
            "pos": [
                170,
                100
            ],
            "size": {
                "0": 140,
                "1": 26
            },
            "flags": {},
            "mode": 0,
            "outputs": [
                {
                    "name": "five",
                    "type": "number",
                    "links": [
                        0
                    ]
                }
            ],
            "properties": {}
        },
        {
            "id": 2,
            "type": "Five",
            "pos": [
                170,
                190
            ],
            "size": {
                "0": 140,
                "1": 26
            },
            "flags": {},
            "mode": 0,
            "outputs": [
                {
                    "name": "five",
                    "type": "number",
                    "links": [
                        1
                    ]
                }
            ],
            "properties": {}
        }
    ],
    "links": [
        [
            0,
            1,
            0,
            3,
            0,
            "number"
        ],
        [
            1,
            2,
            0,
            3,
            1,
            "number"
        ]
    ],
    "groups": [],
    "config": {
        "align_to_grid": true
    },
    "version": 0.4
}"""

ADVANCED_SUM = """{
    "last_node_id": 7,
    "last_link_id": 8,
    "nodes": [
        {
            "id": 1,
            "type": "demo/five",
            "pos": [
                20,
                130
            ],
            "size": {
                "0": 140,
                "1": 26
            },
            "flags": {},
            "mode": 0,
            "outputs": [
                {
                    "name": "five",
                    "type": "number",
                    "links": [
                        0,
                        4
                    ]
                }
            ],
            "properties": {}
        },
        {
            "id": 5,
            "type": "demo/print",
            "pos": [
                590,
                180
            ],
            "size": {
                "0": 140,
                "1": 26
            },
            "flags": {},
            "mode": 0,
            "inputs": [
                {
                    "name": "val",
                    "type": "number",
                    "link": 5
                }
            ],
            "properties": {
                "val": 0
            }
        },
        {
            "id": 6,
            "type": "demo/print",
            "pos": [
                570,
                70
            ],
            "size": {
                "0": 140,
                "1": 26
            },
            "flags": {},
            "mode": 0,
            "inputs": [
                {
                    "name": "val",
                    "type": "number",
                    "link": 7
                }
            ],
            "properties": {
                "val": 0
            }
        },
        {
            "id": 7,
            "type": "demo/multiply",
            "pos": [
                380,
                190
            ],
            "size": {
                "0": 140,
                "1": 46
            },
            "flags": {},
            "mode": 0,
            "inputs": [
                {
                    "name": "num1",
                    "type": "number",
                    "link": 4
                },
                {
                    "name": "num2",
                    "type": "number",
                    "link": 3
                }
            ],
            "outputs": [
                {
                    "name": "product",
                    "type": "number",
                    "links": [
                        5
                    ]
                }
            ],
            "properties": {
                "num1": 0,
                "num2": 0
            }
        },
        {
            "id": 2,
            "type": "demo/sum",
            "pos": [
                260,
                50
            ],
            "size": {
                "0": 210,
                "1": 78
            },
            "flags": {},
            "mode": 0,
            "inputs": [
                {
                    "name": "num1",
                    "type": "number",
                    "link": 0
                },
                {
                    "name": "num2",
                    "type": "number",
                    "link": null
                }
            ],
            "outputs": [
                {
                    "name": "out",
                    "type": "number",
                    "links": [
                        7
                    ]
                }
            ],
            "properties": {
                "num1": 0,
                "num2": 50
            }
        },
        {
            "id": 4,
            "type": "Ssum",
            "pos": [
                80,
                220
            ],
            "size": {
                "0": 210,
                "1": 102
            },
            "flags": {},
            "mode": 0,
            "inputs": [
                {
                    "name": "num1",
                    "type": "number",
                    "link": null
                },
                {
                    "name": "num2",
                    "type": "number",
                    "link": null
                }
            ],
            "outputs": [
                {
                    "name": "out",
                    "type": "number",
                    "links": [
                        3
                    ]
                }
            ],
            "properties": {
                "num1": 10,
                "num2": 90
            }
        }
    ],
    "links": [
        [
            0,
            1,
            0,
            2,
            0,
            "number"
        ],
        [
            3,
            4,
            0,
            7,
            1,
            "number"
        ],
        [
            4,
            1,
            0,
            7,
            0,
            "number"
        ],
        [
            5,
            7,
            0,
            5,
            0,
            "number"
        ],
        [
            7,
            2,
            0,
            6,
            0,
            "number"
        ]
    ],
    "groups": [],
    "config": {
        "align_to_grid": true
    },
    "version": 0.4
}"""