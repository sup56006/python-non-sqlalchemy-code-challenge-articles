# classes/many_to_many.py
from typing import List, Optional


class Author:
    def __init__(self, name: str):
        # use protected attr and go through the setter to validate initial value
        self._name = None
        self.name = name

    # name property: string, len>0, immutable after initial set (further assigns are ignored or validated)
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        # allow setting only if not set yet AND value is valid OR if being set during __init__
        if getattr(self, "_name", None) is None:
            if isinstance(value, str) and len(value) > 0:
                self._name = value
            else:
                # ignore invalid initial assignment (tests expect no exception)
                pass
        else:
            # ignore subsequent assignments (tests do not expect exceptions)
            pass

    def articles(self) -> List["Article"]:
        return [a for a in Article.all if a.author is self]

    def magazines(self) -> List["Magazine"]:
        mags = [a.magazine for a in self.articles()]
        # return unique list preserving insertion order
        seen = []
        for m in mags:
            if m not in seen:
                seen.append(m)
        return seen

    def add_article(self, magazine: "Magazine", title: str) -> "Article":
        return Article(self, magazine, title)

    def topic_areas(self) -> Optional[List[str]]:
        mags = self.magazines()
        if not mags:
            return None
        cats = []
        for m in mags:
            if m.category not in cats:
                cats.append(m.category)
        return cats


class Magazine:
    all: List["Magazine"] = []

    def __init__(self, name: str, category: str):
        # protected attrs
        self._name = None
        self._category = None

        # validate and set via property setters
        self.name = name
        self.category = category

        # register magazine
        Magazine.all.append(self)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        # must be str and length between 2 and 16 inclusive
        if isinstance(value, str) and 2 <= len(value) <= 16:
            # allow both initial and subsequent valid sets
            self._name = value
        else:
            # ignore invalid assignments (tests expect no exception, and unchanged)
            pass

    @property
    def category(self) -> str:
        return self._category

    @category.setter
    def category(self, value):
        # must be str and non-empty
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        else:
            # ignore invalid assignments
            pass

    def articles(self) -> List["Article"]:
        return [a for a in Article.all if a.magazine is self]

    def contributors(self) -> List["Author"]:
        authors = [a.author for a in self.articles()]
        # unique preserve order
        seen = []
        for au in authors:
            if au not in seen:
                seen.append(au)
        return seen

    def article_titles(self) -> Optional[List[str]]:
        titles = [a.title for a in self.articles()]
        return titles if titles else None

    def contributing_authors(self) -> Optional[List["Author"]]:
        if not self.articles():
            return None
        # count articles per author for this magazine
        counts = {}
        for a in self.articles():
            counts[a.author] = counts.get(a.author, 0) + 1
        result = [author for author, cnt in counts.items() if cnt > 2]
        return result if result else None

    @classmethod
    def top_publisher(cls) -> Optional["Magazine"]:
        # returns the magazine with most articles, or None if there are no articles
        if not Article.all:
            return None
        best = None
        best_count = 0
        for mag in cls.all:
            cnt = len(mag.articles())
            if cnt > best_count:
                best = mag
                best_count = cnt
        return best


class Article:
    all: List["Article"] = []

    def __init__(self, author: Author, magazine: Magazine, title: str):
        # protected attributes
        self._author = None
        self._magazine = None
        self._title = None

        # set via properties (validations occur there)
        self.author = author
        self.magazine = magazine
        self.title = title

        # register article
        Article.all.append(self)

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value):
        # title must be str and length 5..50 inclusive
        # set only if not set yet
        if getattr(self, "_title", None) is None:
            if isinstance(value, str) and 5 <= len(value) <= 50:
                self._title = value
            else:
                # ignore invalid; tests expect no exception
                pass
        else:
            # ignore reassignments
            pass

    @property
    def author(self) -> Author:
        return self._author

    @author.setter
    def author(self, value):
        # must be Author; mutable
        if isinstance(value, Author):
            self._author = value
        else:
            # ignore invalid
            pass

    @property
    def magazine(self) -> Magazine:
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        # must be Magazine; mutable
        if isinstance(value, Magazine):
            self._magazine = value
        else:
            # ignore invalid
            pass
