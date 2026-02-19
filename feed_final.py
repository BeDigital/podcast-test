import xml.etree.ElementTree as xml_etree

import yaml


def add_text(parent, tag, value):
  if value is None:
    return
  xml_etree.SubElement(parent, tag).text = str(value)


def main():
  with open("feed.yaml", "r", encoding="utf-8") as file:
    yaml_data = yaml.safe_load(file)

  xml_etree.register_namespace("itunes", "http://www.itunes.com/dtds/podcast-1.0.dtd")
  xml_etree.register_namespace("content", "http://purl.org/rss/1.0/modules/content/")

  rss_element = xml_etree.Element(
    "rss",
    {
      "version": "2.0",
      "xmlns:itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
      "xmlns:content": "http://purl.org/rss/1.0/modules/content/",
    },
  )

  channel_element = xml_etree.SubElement(rss_element, "channel")
  add_text(channel_element, "title", yaml_data.get("title"))
  add_text(channel_element, "description", yaml_data.get("description"))
  add_text(channel_element, "language", yaml_data.get("language"))
  add_text(channel_element, "itunes:subtitle", yaml_data.get("subtitle"))
  add_text(channel_element, "itunes:author", yaml_data.get("author"))

  category = yaml_data.get("category")
  if category:
    xml_etree.SubElement(channel_element, "itunes:category", {"text": str(category)})

  image = yaml_data.get("image")
  if image:
    xml_etree.SubElement(channel_element, "itunes:image", {"href": str(image)})

  for episode in yaml_data.get("item", []):
    item_element = xml_etree.SubElement(channel_element, "item")
    add_text(item_element, "title", episode.get("title"))
    add_text(item_element, "description", episode.get("description"))
    add_text(item_element, "pubDate", episode.get("published"))
    add_text(item_element, "itunes:duration", episode.get("duration"))

    episode_file = episode.get("file")
    if episode_file:
      length = str(episode.get("length", "0")).replace(",", "")
      xml_etree.SubElement(
        item_element,
        "enclosure",
        {
          "url": str(episode_file),
          "length": length,
          "type": str(yaml_data.get("format", "audio/mpeg")),
        },
      )
      add_text(item_element, "guid", episode_file)

  output_tree = xml_etree.ElementTree(rss_element)
  output_tree.write("podcast.xml", encoding="UTF-8", xml_declaration=True)


if __name__ == "__main__":
  main()