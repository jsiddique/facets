import pandas as pd
from IPython.core.magics.display import Javascript
import pkg_resources

resource_package = __name__
resource_path_base = '/base.html'
resource_path_facets = '/facets-jupyter.html'

base_html = pkg_resources.resource_stream(resource_package, resource_path_base).read()
facets_html = pkg_resources.resource_stream(resource_package, resource_path_facets).read()


class Facets():
    def __init__(self):
        """Initialize the class object.

        Initializes the object and pulls the base html file with placeholders
        that will be replaced with a subsequently defined atlas and class labels.
        """
        self.base_html = base_html.decode("utf-8")
        self.html = self.base_html
        self.facets_html = facets_html.decode("utf-8")
        self.atlas_defined = False
        self.classes_defined = False
        self.label_dict = {}

    def reset_facets(self):
        """Reset the facets html string

        Defining classes and and atlas overwrites the placeholders in the self.html
        string used to render the html file. If the atlas or class labels are redefined,
        the html string must be 'reset'.
        """
        self.html = self.base_html

    def define_atlas(self, atlas_df, atlas_height=800, sprite_width=100, sprite_height=100, atlas_url=None):
        """Defines an atlas and inserts the relevant html into the self.html string

        This method is used to define the atlas object which forms the basis of the
        interactive image array in Facets. An atlas dataframe is supplied which
        contains the metadata for the images, along with relevant rendering parameters
        such as sprite dimensions.

        args:
            atlas_df: a pandas datafarme of the atlas metadata. The first column should
                      be a unique id value
        kwargs:
             atlas_height: height of the atlas in pixels (default 800)
             sprite_width: width of each individual image sprite in pixels (default 100)
            sprite_height: height of each individual image sprite in pixels (default 100)
               atlas_file: filepath of the atlas image (default None)

        returns:
            <None>
        """
        if type(atlas_df) != pd.core.frame.DataFrame:
            raise TypeError("You must supply a pandas DataFrame to define the atlas element characteristics.")
        if type(atlas_height) is not int:
            raise TypeError("You must supply an integer value for atlas height.")
        if type(sprite_width) is not int:
            raise TypeError("You must supply an integer value for sprite width.")
        if type(sprite_height) is not int:
            raise TypeError("You must supply an integer value for sprite height.")
        if sprite_width > atlas_height or sprite_height > atlas_height:
            raise ValueError("Sprites cannot be larger than the atlas.")
        if atlas_url is None or type(atlas_url) is not str:
            raise ValueError("You must supply an atlas filepath as a string.")

        self.atlas_df = atlas_df.copy()
        if 'SessionLabel' not in self.atlas_df.columns:
            self.atlas_df['SessionLabel'] = None
        self.html = self.html.replace("{json}", self.atlas_df.to_json(orient="records").replace("\"", "\\\""))
        self.html = self.html.replace("{atlas-height}", str(atlas_height))
        self.html = self.html.replace("{sprite-width}", str(sprite_width))
        self.html = self.html.replace("{sprite-height}", str(sprite_height))
        self.html = self.html.replace("{atlas-url}", atlas_url)
        self.atlas_defined = True

    def render_html(self, filename):
        """Renders the html file used to interact with the Facets environment.

        This writes the html file based on the modified self.html string and is
        what you should then open to explore the atlas. Note that having
        facets-jupyter.html in the same directory is required.
        """
        if self.classes_defined and self.atlas_defined:
            facets_path = filename.split('.html')[0] + '_facets.html'
            self.html = self.html.replace("{reference}", facets_path)
            fp = open(filename, 'w')
            fp.write(self.html)
            fp.close()
            fp = open(facets_path, 'w')
            fp.write(self.facets_html)
            fp.close()
        else:
            raise ValueError("You must define both an atlas and classes before you render the html file.")

    def create_labeled_variables(self, dict_name):
        command = """
            var kernel = IPython.notebook.kernel;
            for (var i=0; i<localStorage.length; i++) {
                var key = localStorage.key(i);
                var existingItem = localStorage.getItem(key);
                var var_name = key;
                if (key === null) {
                    continue
                }
                var values = existingItem.split(',')
                for (var j=0; j<values.length; j++) {
                    var command = "{dict_name}['" + var_name + "'] += ['" + values[j] + "']";
                    kernel.execute(command);
                    kernel.execute("{dict_name}['" + var_name + "'] = list(set({dict_name}['" + var_name + "']))");
                }
            }
        """
        command = command.replace('{dict_name}', dict_name)
        return Javascript(command)

    def create_classes(self, labels):
        """Create the possible classes (labels) for each example.

        Use this method to create the possible classes (labels) for each example of your
        data/atlas. The self.html string will be updated to reflect the possible choices
        and present you with a list of selections that you can choose between when picking
        training examples within Facets. Labels is passed simply as a list of strings.
        """
        if type(labels) is not list:
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
            self.label_dict[label] = []
            javascript_options += " " * 32 + "<a href=\"#\" class=\"class-selector\">" + label + "</a>\n"
            javascript_counters += " " * 20 + "<button style=\"margin-top: 6\" class=\"counter-button\" id=\"counter-" + label + "\"><b>" + label + ":</b> 0" + "</button>\n"
        javascript_counters += " " * 20 + "<button class=\"counter-button-total\" id=\"counter-total\"><b>Total:</b> 0</button>"

        self.html = self.html.replace("{options}", javascript_options)
        self.html = self.html.replace("{option-1}", self.labels[0])
        self.html = self.html.replace("{label-buttons}", javascript_counters)
        self.html = self.html.replace("{first-class}", self.labels[0])
        self.classes_defined = True

        return self.label_dict