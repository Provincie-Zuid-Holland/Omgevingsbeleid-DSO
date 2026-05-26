import pytest

from dso.services.tekst.middleware import middleware_image_in_p


class TestImageInP:
    @pytest.mark.parametrize(
        "input_value, expected_output",
        [
            ("", ""),
            ("text", "text"),
            ("<p>text</p>", "<p>text</p>"),
            (
                "<p>text</p><p>text2</p>",
                """
<p>text</p>
<p>text2</p>
""",
            ),
            (
                "<p>text<strong>text2</strong></p><p>text3</p>",
                """
<p>text<strong>text2</strong></p>
<p>text3</p>
""",
            ),
            (
                "<p>test<img>test2</p>",
                """
<p>test</p>
<img><p>test2</p>
""",
            ),
            (
                "<p>test<img>test2<img>test3</p>",
                """
<p>test</p>
<img><p>test2</p>
<img><p>test3</p>
""",
            ),
            (
                "<p>test<img>test2<strong>test3<img>test4</strong></p>",
                """
<p>test</p>
<img><p>test2<strong>test3<img>test4</strong></p>
""",
            ),
        ],
    )
    def test_middleware_image_in_p(self, input_value: str, expected_output: str) -> None:
        actual_output: str = middleware_image_in_p(input_value)
        assert actual_output == expected_output
