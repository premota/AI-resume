import re


class CleanText:
    def __init__(self, raw_text: str):
        if not isinstance(raw_text, str):
            raise TypeError("raw text must be a string")

        self.raw_text = raw_text
        self.cleaned_text = raw_text

    def remove_excessive_space(self) -> "CleanText":
        """
        Remove excessive spacing from text corpus

        :rtype: str
        """
        self.cleaned_text = re.sub(r"\s+", " ", self.cleaned_text).strip()
        return self

    def lowercasing(self) -> "CleanText":
        self.cleaned_text = self.cleaned_text.lower()
        return self

    def reset(self) -> "CleanText":
        self.cleaned_text = self.raw_text
        return self

    def get_cleaned_text(self) -> str:
        return self.cleaned_text


if __name__ == "__main__":
    import re

    text = "      -my     name is   "
    print(text)
    print(re.sub(r"\s+", " ", text))
