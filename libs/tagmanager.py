import xattr

class TagManager:
    @staticmethod
    def set_tags(file, *tags, name="user.xdg.tags"):
        """
        :param tags: each tag as an argument
        """
        tags = ",".join(set(str(t).strip().zfill(4) for t in tags))
        tags = tags.encode()
        xattr.xattr(file).set(name, tags)

    @staticmethod
    def get_tag_names(filename):
        return xattr.xattr(filename).list()

    @staticmethod
    def get_tags(file, name="user.xdg.tags"):
        """
        :return: set of all tags
        """
        attrs = xattr.xattr(file)

        tags = attrs.get(name).decode() if name in attrs.list() else []
        if tags:
            tags = set(tags.strip().split(","))
        return tags

    @staticmethod
    def add_tags(file, *tags):
        """
        :param tags: each tag as an argument
        """
        old_tags = TagManager.get_tags(file)
        tags = old_tags.union(set(tags))
        TagManager.set_tags(file, *tags)

    @staticmethod
    def has_tag(file, tag):
        return tag in TagManager.get_tag_names(file)

    @staticmethod
    def has_tags(file):
        return bool(TagManager.get_tag_names(file))
