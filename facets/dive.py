import js2py
import pandas as pd

class Facets():
    def __init__(self):
        self.html = """
            <head>
                <link rel="import" href="./facets-jupyter.html"></link>
            </head>
            
            <table style="width:100%">
                <tr>
                    <th style="width:15%"></th>
                    <th style="width:10%"></th>
                    <th style="width:75%"><h1 id="msg_1" style="color:red">Selecting ----</h1></th>
                </tr>
                <tr>
                    <th>
                        Select Class:
                        <select id="ClassValue">
                            {options}
                        </select>
                    </th>
                    <th>
                        <input type="button" onClick="ClearEverything()", value="Reset">
                    </th>
                    <th></th>
                </tr>
            </table>
            <p></p>
            
            <table style="width:100%">
                <tr>{counters}</tr>
            </table>
            
            <facets-dive id="elem" height="{height}" sprite-image-width="{sprite-width}" sprite-image-height="{sprite-height}" atlas-url="{atlas-url}"></facets-dive>
            <script>
                var data = JSON.parse("{json}");
                
                document.querySelector("#elem").data = data;
                document.getElementById("elem").addEventListener("click", function(e) {
                    if (e.ctrlKey) {
                        var e = document.getElementById("ClassValue");
                        var keyVal = e.options[e.selectedIndex].value;
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
                function ClearEverything(){
                    for (var i=0; i<localStorage.length; i++){
                        var keyVal = localStorage.key();
                        var element = document.getElementById(keyVal);
                        element.innerHTML = keyVal + " : 0";
                        element.style.color = "black"
                    }
                }
            </script>
        """
        self.base_html = self.html
        
    def reset_facets(self):
        self.html = self.base_html
        
        
    def define_atlas(self, atlas_df, atlas_height=800, sprite_width=100, sprite_height=100):
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
        
        self.atlas_df = atlas_df
        self.html = self.html.replace("{json}", self.atlas_df.to_json(orient="records").replace("\"", "\\\""))

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
            if i != len(self.labels) - 1:
                javascript_options += " "*20 + "<option value=\"" + label + "\">" + label + "</option>\n"
                javascript_counters+= "<th><b id=\"" + label + "\">" + label + ": 0</b></th>\n"
            else:
                javascript_options += "<option value=\"" + label + "\">" + label + "</option>"
                javascript_counters+= "<th><b id=\"" + label + "\">" + label + ": 0</b></th>"
        
        self.html = self.html.replace("{options}", javascript_options)
        self.html = self.html.replace("{counters}", javascript_counters)
        
        
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