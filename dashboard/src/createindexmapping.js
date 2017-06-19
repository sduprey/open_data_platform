"use strict";


module.exports = function(client){
    return new Promise(function(resolve, reject){

        var body = {
            "mappings": {

                "iris": {
                    properties : {
                        "boulodromes": {"type" : "float"},
                        "skate": {"type" : "float"},
                        "golf": {"type" : "float"},
                        "departement": {"type" : "string", "index": "not_analyzed"},
                        "geometry": {"type" : "geo_shape"},
                        "center": {"type" : "geo_point"}

//                        "boulodromes": {"type" : "float",     "store" : true },
//                        "skate": {"type" : "float",    "store" : true },
//                        "golf": {"type" : "float",    "store" : true },
//                        "departement": {"type" : "string",    "store" : true, "index": "not_analyzed"},
//                        "geometry": {"type" : "geo_shape", "store" : true },
//                        "center": {"type" : "geo_point", "store" : true }
                    }
                }
            }
        };
        console.log("Creating up the former indice");

        client.indices.create(
            {
                index: "iris",
                body: body
            }
            , function (error) {
                if (error) {
                    reject(error);
                }
                else {
                    console.log("Created iris index with mapping.")
                    resolve();
                }
            }
        );

    })
}
                



