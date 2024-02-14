import shutil
import tempfile
import os.path
from ..check_chameleon import main, attribute, NSMAP
from testfixtures import OutputCapture

import lxml.etree
import os
import unittest

LINK_MISSING_HREF = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a>Link</a>
  </body>
</html>
"""

LINK_SINGLE_FRAGMENT_IDENTIFIER = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a href="#">Link</a>
  </body>
</html>
"""

LINK_ROLE_BUTTON = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a role="button" href="#">Link</a>
  </body>
</html>
"""

LINK_ROLE_BUTTON_MISSING_HREF = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a role="button">Link</a>
  </body>
</html>
"""

LINK_HREF = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a href="link.html">Link</a>
  </body>
</html>
"""

LINK_TALATTR_HREF = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a tal:attributes="
        name 'Name';
        title 'Title';
        href 'link.html'">Link</a>
  </body>
</html>
"""

LINK_X_NG_ATTR = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a x-ng-href="expression">Link</a>
  </body>
</html>
"""

LINK_TEXT_CONTENT = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a href="link.html">Link</a>
  </body>
</html>
"""

LINK_TAL_CONTENT_LINK_NODE = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a href="link.html" tal:content="'Link'"></a>
  </body>
</html>
"""

LINK_TAL_CONTENT_CHILD_NODE = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a href="link.html"><span tal:content="'Link'"></span></a>
  </body>
</html>
"""

LINK_TAL_REPLACE_CHILD_NODE = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a href="link.html"><tal:block replace="'Link'"></tal:block></a>
  </body>
</html>
"""

LINK_TAL_REPLACE_CHILD_NODE2 = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a href="link.html"><span tal:replace="'Link'"></span></a>
  </body>
</html>
"""

LINK_IMG_CONTENT = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a href="link.html"><img src="image.png" alt="Link"/></a>
  </body>
</html>
"""

LINK_ARIA_LABEL_CONTENT = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a href="link.html" aria-label="Link"></a>
  </body>
</html>
"""

LINK_NO_TEXT_CONTENT = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a href="link.html"></a>
  </body>
</html>
"""

IMG_MISSING_ALT = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <img src="image.png"/>
  </body>
</html>
"""

BUTTON_TEXT_CONTENT = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <button>Actionable</button>
  </body>
</html>
"""

BUTTON_NO_CONTENT = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <button><i class="fa-nice-button"></i></button>
  </body>
</html>
"""

BUTTON_TAL_CONTENT_BUTTON_NODE = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <button tal:content="'Link'"></button>
  </body>
</html>
"""

BUTTON_TAL_CONTENT_CHILD_NODE = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <button><span tal:content="'Link'"></span></button>
  </body>
</html>
"""

LABEL_WITHOUT_FOR_ATTRIBUTE = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <label>Label text</label><input type="text"/>
  </body>
</html>
"""

LABEL_WITH_FOR_ATTRIBUTE = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <label for="inputid">Label text</label><input id="inputid" type="text"/>
  </body>
</html>
"""

LABEL_WITH_XNG_ATTR_FOR = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <input id="inputid" type="text"/>
    <label x-ng-attr-for="inputid">Label text</label>
  </body>
</html>
"""

LABEL_WRAPS_INPUT = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <label><input type="text"/>Label text</label>
  </body>
</html>
"""


class TestAttributeHelper(unittest.TestCase):
    def test_attribute_found(self):
        node = lxml.etree.fromstring(
            "<html"
            '  xmlns="http://www.w3.org/1999/xhtml"'
            '  xmlns:tal="http://xml.zope.org/namespaces/tal">'
            "  <body>"
            '    <div class="foo">body contents</div>'
            "  </body>"
            "</html>"
        ).xpath("/xhtml:html/xhtml:body/xhtml:div", namespaces=NSMAP)[0]
        self.assertEqual("foo", attribute(node, "class"))

    def test_attribute_missing(self):
        node = lxml.etree.fromstring(
            "<html"
            '  xmlns="http://www.w3.org/1999/xhtml"'
            '  xmlns:tal="http://xml.zope.org/namespaces/tal">'
            "  <body>"
            '    <div notaclass="foo">body contents</div>'
            "  </body>"
            "</html>"
        ).xpath("/xhtml:html/xhtml:body/xhtml:div", namespaces=NSMAP)[0]
        self.assertIsNone(attribute(node, "class"))

    def test_attribute_wrong_namespace(self):
        node = lxml.etree.fromstring(
            "<html"
            '  xmlns="http://www.w3.org/1999/xhtml"'
            '  xmlns:tal="http://xml.zope.org/namespaces/tal">'
            "  <body>"
            "    <div attributes=\"class 'foo'\">body contents</div>"
            "  </body>"
            "</html>"
        ).xpath("/xhtml:html/xhtml:body/xhtml:div", namespaces=NSMAP)[0]
        self.assertIsNone(attribute(node, "class"))

    def test_attribute_x_ng_attribute(self):
        node = lxml.etree.fromstring(
            "<html"
            '  xmlns="http://www.w3.org/1999/xhtml"'
            '  xmlns:tal="http://xml.zope.org/namespaces/tal">'
            "  <body>"
            '    <div x-ng-class="{{foo}}">body contents</div>'
            "  </body>"
            "</html>"
        ).xpath("/xhtml:html/xhtml:body/xhtml:div", namespaces=NSMAP)[0]
        self.assertEqual("{{foo}}", attribute(node, "class"))

    def test_attribute_x_ng_attribute_missing(self):
        node = lxml.etree.fromstring(
            "<html"
            '  xmlns="http://www.w3.org/1999/xhtml"'
            '  xmlns:tal="http://xml.zope.org/namespaces/tal">'
            "  <body>"
            '    <div x-ng-notaclass="{{foo}}">body contents</div>'
            "  </body>"
            "</html>"
        ).xpath("/xhtml:html/xhtml:body/xhtml:div", namespaces=NSMAP)[0]
        self.assertIsNone(attribute(node, "class"))

    def test_attribute_tal_attributes(self):
        node = lxml.etree.fromstring(
            "<html"
            '  xmlns="http://www.w3.org/1999/xhtml"'
            '  xmlns:tal="http://xml.zope.org/namespaces/tal">'
            "  <body>"
            "    <div tal:attributes=\"class 'foo'\">body contents</div>"
            "  </body>"
            "</html>"
        ).xpath("/xhtml:html/xhtml:body/xhtml:div", namespaces=NSMAP)[0]
        self.assertEqual("'foo'", attribute(node, "class"))

    def test_attribute_tal_attributes_multiline_single_attr(self):
        node = lxml.etree.fromstring(
            "<html"
            '  xmlns="http://www.w3.org/1999/xhtml"'
            '  xmlns:tal="http://xml.zope.org/namespaces/tal">'
            "  <body>"
            '    <div tal:attributes="'
            "      class 'foo'\">body contents</div>"
            "  </body>"
            "</html>"
        ).xpath("/xhtml:html/xhtml:body/xhtml:div", namespaces=NSMAP)[0]
        self.assertEqual("'foo'", attribute(node, "class"))

    def test_attribute_tal_attributes_multiline_multiple_attr(self):
        node = lxml.etree.fromstring(
            """<html
              xmlns="http://www.w3.org/1999/xhtml"
              xmlns:tal="http://xml.zope.org/namespaces/tal">
              <body>
                <div tal:attributes="
                  id 'some-id';
                  class 'foo';
                  title 'Some Title'">body contents</div>
              </body>
            </html>"""
        ).xpath("/xhtml:html/xhtml:body/xhtml:div", namespaces=NSMAP)[0]
        self.assertEqual("'foo'", attribute(node, "class"))

    def test_attribute_tal_attributes_singleline_multiple_attr(self):
        node = lxml.etree.fromstring(
            "<html"
            '  xmlns="http://www.w3.org/1999/xhtml"'
            '  xmlns:tal="http://xml.zope.org/namespaces/tal">'
            "  <body>"
            '    <div tal:attributes="'
            "      id 'some-id'; class 'foo'; title 'Some Title'\">"
            "      body contents"
            "    </div>"
            "  </body>"
            "</html>"
        ).xpath("/xhtml:html/xhtml:body/xhtml:div", namespaces=NSMAP)[0]
        self.assertEqual("'foo'", attribute(node, "class"))

    def test_attribute_tal_attributes_multiline_extraneous_whitespace(self):
        node = lxml.etree.fromstring(
            "<html"
            '  xmlns="http://www.w3.org/1999/xhtml"'
            '  xmlns:tal="http://xml.zope.org/namespaces/tal">'
            "  <body>"
            '    <div tal:attributes="'
            "      id 'some-id'; class 'foo'     ; title 'Some Title'\">"
            "      body contents"
            "    </div>"
            "  </body>"
            "</html>"
        ).xpath("/xhtml:html/xhtml:body/xhtml:div", namespaces=NSMAP)[0]
        self.assertEqual("'foo'", attribute(node, "class"))

    def test_attribute_tal_attributes_attr_name_substring(self):
        node = lxml.etree.fromstring(
            """<html
              xmlns="http://www.w3.org/1999/xhtml"
              xmlns:tal="http://xml.zope.org/namespaces/tal">
              <body>
                <div tal:attributes="
                  id 'some-id';
                  classy 'foo';
                  title 'Some Title'">body contents</div>
              </body>
            </html>"""
        ).xpath("/xhtml:html/xhtml:body/xhtml:div", namespaces=NSMAP)[0]
        self.assertIsNone(attribute(node, "class"))


class TestA11yLint(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.directory)

    def given_a_file_in_test_dir(self, filename: str, content: str) -> str:
        filename = os.path.join(self.directory, filename)
        with open(filename, "w+") as stream:
            stream.write(content)
        return filename

    def test_invalid_template(self):
        filename = self.given_a_file_in_test_dir("invalid.cpt", "gibberish")
        with OutputCapture():
            self.assertEqual(main([filename]), 1)

    def test_link_requires_href(self):
        filename = self.given_a_file_in_test_dir("invalid.cpt", LINK_MISSING_HREF)
        with OutputCapture():
            self.assertEqual(main([filename]), 1)

    def test_link_href_fragment(self):
        filename = self.given_a_file_in_test_dir(
            "invalid.cpt", LINK_SINGLE_FRAGMENT_IDENTIFIER
        )
        with OutputCapture():
            self.assertEqual(main([filename]), 1)

    def test_link_role_button(self):
        filename = self.given_a_file_in_test_dir("valid.cpt", LINK_ROLE_BUTTON)
        with OutputCapture():
            self.assertEqual(main([filename]), 0)

    def test_link_role_button_requires_href(self):
        filename = self.given_a_file_in_test_dir(
            "invalid.cpt", LINK_ROLE_BUTTON_MISSING_HREF
        )
        with OutputCapture():
            self.assertEqual(main([filename]), 1)

    def test_link_has_href(self):
        filename = self.given_a_file_in_test_dir("valid.cpt", LINK_HREF)
        with OutputCapture():
            self.assertEqual(main([filename]), 0)

    def test_link_has_href_tal_attributes(self):
        filename = self.given_a_file_in_test_dir("valid.cpt", LINK_TALATTR_HREF)
        with OutputCapture():
            self.assertEqual(main([filename]), 0)

    def test_link_has_href_angular_attribute(self):
        filename = self.given_a_file_in_test_dir("valid.cpt", LINK_X_NG_ATTR)
        with OutputCapture():
            self.assertEqual(main([filename]), 0)

    def test_link_has_img_content(self):
        filename = self.given_a_file_in_test_dir("valid.cpt", LINK_IMG_CONTENT)
        with OutputCapture():
            self.assertEqual(main([filename]), 0)

    def test_link_has_aria_label_content(self):
        filename = self.given_a_file_in_test_dir("valid.cpt", LINK_ARIA_LABEL_CONTENT)
        with OutputCapture():
            self.assertEqual(main([filename]), 0)

    def test_link_has_text_content(self):
        filename = self.given_a_file_in_test_dir("valid.cpt", LINK_TEXT_CONTENT)
        with OutputCapture():
            self.assertEqual(main([filename]), 0)

    def test_link_has_tal_content_link_node(self):
        filename = self.given_a_file_in_test_dir(
            "valid.cpt", LINK_TAL_CONTENT_LINK_NODE
        )
        with OutputCapture():
            self.assertEqual(main([filename]), 0)

    def test_link_has_tal_content_child_node(self):
        filename = self.given_a_file_in_test_dir(
            "valid.cpt", LINK_TAL_CONTENT_CHILD_NODE
        )
        with OutputCapture():
            self.assertEqual(main([filename]), 0)

    def test_link_has_tal_replace_child_node(self):
        filename = self.given_a_file_in_test_dir(
            "valid.cpt", LINK_TAL_REPLACE_CHILD_NODE
        )
        with OutputCapture():
            self.assertEqual(main([filename]), 0)
        filename = self.given_a_file_in_test_dir(
            "valid.cpt", LINK_TAL_REPLACE_CHILD_NODE2
        )
        with OutputCapture():
            self.assertEqual(main([filename]), 0)

    def test_link_has_no_text_content(self):
        filename = self.given_a_file_in_test_dir("invalid.cpt", LINK_NO_TEXT_CONTENT)
        with OutputCapture():
            self.assertEqual(main([filename]), 1)

    def test_img_requires_alt(self):
        filename = self.given_a_file_in_test_dir("invalid.cpt", IMG_MISSING_ALT)
        with OutputCapture():
            self.assertEqual(main([filename]), 1)

    def test_button_has_text_content(self):
        filename = self.given_a_file_in_test_dir("valid.cpt", BUTTON_TEXT_CONTENT)
        with OutputCapture():
            self.assertEqual(main([filename]), 0)

    def test_button_has_no_text_content(self):
        filename = self.given_a_file_in_test_dir("invalid.cpt", BUTTON_NO_CONTENT)
        with OutputCapture():
            self.assertEqual(main([filename]), 1)

    def test_button_has_tal_content_link_node(self):
        filename = self.given_a_file_in_test_dir(
            "valid.cpt", BUTTON_TAL_CONTENT_BUTTON_NODE
        )
        with OutputCapture():
            self.assertEqual(main([filename]), 0)

    def test_button_has_tal_content_child_node(self):
        filename = self.given_a_file_in_test_dir(
            "valid.cpt", BUTTON_TAL_CONTENT_CHILD_NODE
        )
        with OutputCapture():
            self.assertEqual(main([filename]), 0)

    def test_label_has_no_for_attribute(self):
        filename = self.given_a_file_in_test_dir(
            "invalid.cpt", LABEL_WITHOUT_FOR_ATTRIBUTE
        )
        with OutputCapture():
            self.assertEqual(main([filename]), 1)

    def test_label_has_for_attribute(self):
        filename = self.given_a_file_in_test_dir("valid.cpt", LABEL_WITH_FOR_ATTRIBUTE)
        with OutputCapture():
            self.assertEqual(main([filename]), 0)

    def test_label_has_xng_attr_for_attribute(self):
        filename = self.given_a_file_in_test_dir("valid.cpt", LABEL_WITH_XNG_ATTR_FOR)
        with OutputCapture():
            self.assertEqual(main([filename]), 0)

    def test_label_wraps_input(self):
        filename = self.given_a_file_in_test_dir("valid.cpt", LABEL_WRAPS_INPUT)
        with OutputCapture():
            self.assertEqual(main([filename]), 0)
