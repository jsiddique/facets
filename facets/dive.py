import js2py
import pandas as pd

class Facets():
    def __init__(self):
        self.html = """
        <meta http-equiv="Content-Type" content="text/html; charset=utf-16">
        <html>
            <head>
                <link rel="import" href="./facets-jupyter.html"></link>
                <style>
                    .button {
                        background-color: #d73027;
                        color: #FFFFFF;
                        padding: 10px;
                        font-size: 24px;
                        border: none;
                        cursor: pointer;
                        border-radius: 8px;
                        display: inline-block;
                        width: 153px;
                        transition: all 0.5s;
                        outline: none;
                    }
                    .button span {
                        cursor: pointer;
                        display: inline-block;
                        position: relative;
                        transition: 0.5s;
                        outline: none;
                    }
                    .counter-button {
                        padding: 10px;
                        font-size: 16px;
                        border: none;
                        cursor: pointer;
                        border-radius: 6px;
                        display: inline-block;
                        outline: none;
                        background-color: #d9d9d9;
                    }
                    .counter-button-total {
                        background-color: #addd8e;
                        padding: 10px;
                        font-size: 16px;
                        border: none;
                        cursor: pointer;
                        border-radius: 6px;
                        display: inline-block;
                        outline: none;
                    }

                    .button span:after {
                        content: "»";
                        position: absolute;
                        opacity: 0;
                        top: 0;
                        right: -20px;
                        transition: 0.5s;
                        outline: none;
                    }

                    .button:hover span {
                        padding-right: 25px;
                        outline: none;
                    }
                    .button:hover span:after {
                        opacity: 1;
                        right: 0;
                        outline: none;
                    }
                    .dropbtn {
                        background-color: #1a9850;
                        color: #FFFFFF;
                        padding: 10px;
                        font-size: 24px;
                        border: none;
                        cursor: pointer;
                        border-radius: 8px;
                        outline: none;
                    }
                    .dropdown {
                        position: relative;
                        display: inline-block;
                        outline: none;
                    }
                    .dropdown-content {
                        display: none;
                        position: absolute;
                        background-color: #f9f9f9;
                        width: 100%;
                        box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
                        z-index: 1;
                        outline: none;
                    }
                    .dropdown-content a {
                        color: black;
                        padding: 12px 16px;
                        text-decoration: none;
                        display: block;
                        outline: none;
                    }
                    .dropdown-content a:hover {background-color: #f1f1f1}
                    .dropdown:hover .dropdown-content {
                        display: block;
                        outline: none;
                    }
                    .dropdown:hover .dropbtn {
                        background-color: #006837;
                        outline: none;
                    }
                </style>
            </head>
            <body>
                <table style="width: 100%">
                    <tr>
                        <td align="center">
                            <button class="button" id="reset-button"><span>Reset </span></button>
                                <div class="dropdown">
                                    <button class="dropbtn" id="classselectbutton">Select Class</button>
                                    <div class="dropdown-content">
                                {options}
                                    </div>
                                </div>
                            </td>
                    </tr>
                    <tr>
                        <td align="center">
                            {label-buttons}
                        </td>
                    </tr>
                    <tr>
                        <td align="center">
                            <div style="width: 100%; background-color: #525252; height: 3px; margin-top:6px"></div>
                        </td>
                    </tr>
                </table>

                <facets-dive id="elem" height="800" sprite-image-width="28" sprite-image-height="28" atlas-url="atlas.jpg"></facets-dive>
            </body>
            <script>
                var selectedClass = null;
                var data = JSON.parse("{json}");
                
                var totalLength = 0;
                document.querySelector("#elem").data = data;
                document.getElementById("elem").addEventListener("click", function(e) {
                    if (!!selectedClass) {
                        if (e.ctrlKey) {
                            var keyVal = selectedClass;
                            var theAnchorText = document.getElementById("infoCard").querySelector("dd").innerHTML;
                            var existingItem = localStorage.getItem(keyVal);
                            var found = false;
                            for (var i=0; i<localStorage.length; i++){
                                var tempKeyVal = localStorage.key(i);
                                var tempExistingItem = localStorage.getItem(tempKeyVal);
                                if (tempExistingItem) {
                                    var itemList = tempExistingItem.split(',')
                                    for (var i = 0; i < itemList.length && !found; i++) {
                                        if (itemList[i] === theAnchorText) {
                                            found = true;
                                            break;
                                        };
                                    };
                                };
                            };
                            
                            if (!found) {
                                totalLength += 1;
                                if (!existingItem) {
                                    existingItem = theAnchorText;
                                } else {
                                    existingItem = (existingItem || "") + "," + theAnchorText;
                                };
                                localStorage.setItem(keyVal, existingItem);
                                var element = document.getElementById("counter-" + keyVal);
                                var total_element = document.getElementById("counter-total");
                                element.innerHTML = "<b>" + keyVal + ":</b> " + existingItem.split(",").length;
                                total_element.innerHTML = "<b>Total:</b> " + totalLength;
                            };
                        };
                    }
                });
                document.getElementById("reset-button").addEventListener("click", function(e) {
                    for (var i=0; i<localStorage.length; i++){
                        var keyVal = localStorage.key(i);
                        var element = document.getElementById("counter-" + keyVal);
                        element.innerHTML = "<b>" + keyVal + ":</b> 0";
                        var element_button = document.getElementById("classselectbutton");
                        element_button.innerHTML = "Select Class";
                        totalLength = 0;
                        selectedClass = null;
                    };
                    var total_element = document.getElementById("counter-total");
                    total_element.innerHTML = "<b>Total:</b> 0";
                    localStorage.clear();
                    
                    var counterIds = document.getElementsByClassName('counter-button');
                    for (var i = 0; i < counterIds.length; i++) {
                        counterIds[i].style.backgroundColor = '#d9d9d9';
                    };
                });
                
                var classname = document.getElementsByClassName("class-selector");
                for (var i = 0; i < classname.length; i++) {
                    classname[i].addEventListener('click', function(e) {
                        var classNameVal = this.innerHTML;
                        var keyVal = classNameVal;
                        selectedClass = keyVal;
                        var element_button = document.getElementById("classselectbutton");
                        element_button.innerHTML = "Select Class: " + selectedClass;
                        var counterIds = document.getElementsByClassName('counter-button');
                        for (var i = 0; i < counterIds.length; i++) {
                            if (counterIds[i].id == 'counter-' + keyVal) {
                                counterIds[i].style.backgroundColor = '#1a9850';
                            } else {
                                counterIds[i].style.backgroundColor = '#d9d9d9';
                            };
                        };
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
        fp = open(filename, 'wb')
        fp.write(self.html.encode('utf8'))
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
            javascript_options += "<a href=\"#\" class=\"class-selector\">" + label + "</a>\n"
            javascript_counters+= "<button style=\"margin-top: 6\" class=\"counter-button\" id=\"counter-" + label + "\"><b>" + label + ":</b> 0" + "</button>\n"
        javascript_counters += "<button class=\"counter-button-total\" id=\"counter-total\"><b>Total:</b> 0</button>"
        
        self.html = self.html.replace("{options}", javascript_options)
        self.html = self.html.replace("{option-1}", self.labels[0])
        self.html = self.html.replace("{label-buttons}", javascript_counters)
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
        
if __name__ == '__main__':
    from tensorflow.examples.tutorials.mnist import input_data
    import sklearn
    from PIL import Image
    import pandas as pd
    
    mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
    x, y = mnist.train.next_batch(60000)
    x, y = sklearn.utils.shuffle(x, y, random_state=0)
    x = x.reshape((x.shape[0], 28, 28, 1))
    x_test, y_test = mnist.test.next_batch(10000)
    x_test = x_test.reshape((x_test.shape[0], 28, 28, 1))
    
    def array_to_sprite_atlas(image_array, num_sprites_x, num_sprites_y):
        "Takes an array of images of shape (num_images, img_width, img_height) and splices them together to form a big ass mosaic (sprite atlas)."
        # Mnist arrays are in 0-1 range, PIL needs 0-255
        image_array = image_array * 255
        image_width, image_height = image_array.shape[1], image_array.shape[2]
        atlas_width  = num_sprites_x * image_width
        atlas_height = num_sprites_y * image_height
        # We paste the samples to get indices arranged in the following way:
        # | 0 | 1 | 2 | 3 |
        # | 4 | 5 | 6 | 7 |
        atlas  = Image.new("RGB", (atlas_width, atlas_height), (0, 0, 0))
        for i in range(num_sprites_y): 
            for j in range(num_sprites_x):
                sample = image_array[num_sprites_x * i + j, :, :]
                image = Image.fromarray(sample)
                atlas.paste(image, (j*image_width, i*image_height))
        return atlas
    atlas = array_to_sprite_atlas(x_test.reshape(x_test.shape[0], 28, 28), 100, 100)
    atlas.save("atlas.jpg", "JPEG")
    
    df = pd.DataFrame()
    df['Id'] = [x for x in range(len(x_test))]
    jsonstr = df.to_json(orient='records')

    fc = Facets()
    fc.create_classes(labels=[str(x) for x in range(0,10)])
    fc.define_atlas(df, sprite_width=28, sprite_height=28, atlas_file='atlas.jpg')
    fc.render_html('testing.html')