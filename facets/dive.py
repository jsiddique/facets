import js2py
import pandas as pd

class Facets():
    def __init__(self):
        self.html = """
        <meta http-equiv="Content-Type" content="text/html; charset=utf-16">
        <!DOCTYPE html>
        <html>
            <head>
                <link rel="import" href="./facets-jupyter.html"></link>
                <style>
                    .button {
                        display: inline-block;
                        border-radius: 8px;
                        background-color: #f4511e;
                        border: none;
                        color: #FFFFFF;
                        text-align: center;
                        font-size: 24px;
                        padding: 10px;
                        width: 150px;
                        transition: all 0.5s;
                        cursor: pointer;
                        margin: 5px;
                    }

                    .button span {
                        cursor: pointer;
                        display: inline-block;
                        position: relative;
                        transition: 0.5s;
                    }

                    .button span:after {
                        content: "»";
                        position: absolute;
                        opacity: 0;
                        top: 0;
                        right: -20px;
                        transition: 0.5s;
                    }

                    .button:hover span {
                        padding-right: 25px;
                    }

                    .button:hover span:after {
                        opacity: 1;
                        right: 0;
                    }
                    .dropbtn {
                        background-color: #f4511e;
                        color: #FFFFFF;
                        padding: 10px;
                        font-size: 24px;
                        border: none;
                        cursor: pointer;
                        border-radius: 8px;
                    }

                    .dropdown {
                        position: relative;
                        display: inline-block;
                    }

                    .dropdown-content {
                        display: none;
                        position: absolute;
                        background-color: #f9f9f9;
                        min-width: 160px;
                        box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
                        z-index: 1;
                    }

                    .dropdown-content a {
                        color: black;
                        padding: 12px 16px;
                        text-decoration: none;
                        display: block;
                    }

                    .dropdown-content a:hover {background-color: #f1f1f1}

                    .dropdown:hover .dropdown-content {
                        display: block;
                    }

                    .dropdown:hover .dropbtn {
                        background-color: #3e8e41;
                    }
                </style>
            </head>
            <body>
                <table style="width:100%">
                    <tr>
                        <th style="width:15%"></th>
                        <th style="width:10%"></th>
                        <th style="width:75%"><h1 id="msg_1" style="color:red">Selecting Class: {option-1}</h1></th>
                    </tr>
                    <tr>
                        <th>
                        <div class="dropdown">
                            <button class="dropbtn">Select Class</button>
                            <div class="dropdown-content">
                                {options}
                            </div>
                        </div>
                        </th>
                        <th>
                            <button class="button" id="reset-button" style="vertical-align:middle"><span>Reset </span></button>
                        </th>
                        <th></th>
                    </tr>
                </table>
                <p></p>

                <table style="width:100%">
                    <tr>
                        {counters}
                    </tr>
                </table>

                <facets-dive id="elem" height="{height}" sprite-image-width="{sprite-width}" sprite-image-height="{sprite-height}" atlas-url="{atlas-url}"></facets-dive>
            </body>
            <script>
                var selectedClass = {first-class};
                var data = JSON.parse("{json}");
                
                document.querySelector("#elem").data = data;
                document.getElementById("elem").addEventListener("click", function(e) {
                    if (e.ctrlKey) {
                        var keyVal = selectedClass;
                        var theAnchorText = document.getElementById("infoCard").querySelector("dd").innerHTML;
                        var existingItem = localStorage.getItem(keyVal);
                        if (!existingItem) {
                            existingItem = theAnchorText;
                        } else {
                            existingItem = (existingItem || "") + "," + theAnchorText;
                        };
                        localStorage.setItem(keyVal, existingItem);
                        var element = document.getElementById(keyVal);
                        element.innerHTML = keyVal + " : " + existingItem.split(",").length;
                    };
                });
                document.getElementById("reset-button").addEventListener("click", function(e) {
                  
                    for (var i=0; i<localStorage.length; i++){
                        var keyVal = localStorage.key(i);
                        var element = document.getElementById(keyVal);
                        element.innerHTML = keyVal + " : 0";
                        element.style.color = "black"
                    }
                });
                
                var classname = document.getElementsByClassName("class-selector");
                for (var i = 0; i < classname.length; i++) {
                    classname[i].addEventListener('click', function(e) {
                        var classNameVal = this.innerHTML;
                        var keyVal = classNameVal;
                        var element = document.getElementById("msg_1");
                        element.innerHTML = "Selecting: " + keyVal;
                        selectedClass = keyVal;
                    });
                };
            </script>
        </html>
        """
        self.base_html = self.html
        
    def reset_facets(self):
        self.html = self.base_html
        
        
    def define_atlas(self, atlas_df, atlas_height=800, sprite_width=100, sprite_height=100, atlas_file=None):
        if type(df) != pd.core.frame.DataFrame:
            raise TypeError("You must supply a pandas DataFrame to define the atlas element characteristics.")
        if type(atlas_height) is not int:
            raise TypeError("You must supply an integer value for atlas height.")
        if type(sprite_width) is not int:
            raise TypeError("You must supply an integer value for sprite width.")
        if type(sprite_height) is not int:
            raise TypeError("You must supply an integer value for sprite height.")
        if sprite_width > atlas_height or sprite_height > atlas_height:
            raise ValueError("Sprites cannot be larger than the atlas.")
        if atlas_file is None:
            raise ValueError("You must supply an atlas file location.")
        
        self.atlas_df = atlas_df
        self.html = self.html.replace("{json}", self.atlas_df.to_json(orient="records").replace("\"", "\\\""))
        self.html = self.html.replace("{height}", str(atlas_height))
        self.html = self.html.replace("{sprite-width}", str(sprite_width))
        self.html = self.html.replace("{sprite-height}", str(sprite_height))
        self.html = self.html.replace("{atlas-url}", atlas_file)
                                      
                                      
    def render_html(self, filename):
        fp = open(filename, 'w')
        fp.write(self.html)
        fp.close()
        
    def create_classes(self, labels=None):
        if labels is None:
            raise ValueError("You must supply at least two labels.")
        elif type(labels) is not list:
            raise TypeError("Labels must be passed as a list of strings.")
        else:
            if len(labels) < 2:
                raise ValueError("You must supply at least two labels.")
            types = [type(x) for x in labels]
            for x in types:
                if x is not str:
                    raise TypeError("Labels must be passed as a list of strings.")
            
        self.labels = labels
        
        javascript_options = ""
        javascript_counters = ""
        for i, label in enumerate(self.labels):
            if i == 0:
                javascript_options += "<a href=\"#\" class=\"class-selector\">" + label + "</a>\n"
                javascript_counters+= "<th><b id=\"" + label + "\">" + label + ": 0</b></th>\n"
            elif i != len(self.labels) - 1:
                javascript_options += " "*28 + "<a href=\"#\" class=\"class-selector\">" + label + "</a>\n"
                javascript_counters+= " "*20 + "<th><b id=\"" + label + "\">" + label + ": 0</b></th>\n"
            else:
                javascript_options += " "*28 + "<a href=\"#\" class=\"class-selector\">" + label + "</a>"
                javascript_counters+= " "*20 + "<th><b id=\"" + label + "\">" + label + ": 0</b></th>"
        
        self.html = self.html.replace("{options}", javascript_options)
        self.html = self.html.replace("{option-1}", self.labels[0])
        self.html = self.html.replace("{counters}", javascript_counters)
        self.html = self.html.replace("{first-class}", self.labels[0])
        
        
    def return_labels(self):
        js_string = """
            function return_labels(){
                for (var i=0; i<localStorage.length; i++){
                    var key = localStorage.key(i);
                    var existingItem = localStorage.getItem(key);
                    if (key === null) {
                        continue
                    };
                    var values = existingItem.replace("\n\", " ").replace("\r", " ");
                    return values;
                };
            };
            return_labels()
        """
        labels = js2py.eval_js(js_string)
        return labels