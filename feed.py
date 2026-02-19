import yaml
import xml.etree.ElementTree as xml_etree

with open("feed.yaml", "r", encoding="utf-8") as file:
    yaml_data = yaml.safe_load(file)

rss_element = xml_etree.Element('rss', {'version':'2.0',
  'xmlns:itunes':'http://www.itunes.com/dtds/podcast-1.0.dtd',
  'xmlns:content':'http://purl.org/rss/1.0/modules/content/'})

channel_element = xml_etree.SubElement(rss_element, 'channel')

link_prefix = yaml_data['link']

xml_etree.SubElement(channel_element, 'title').text = yaml_data['title']
xml_etree.SubElement(channel_element, 'format').text = yaml_data['format']
xml_etree.SubElement(channel_element, 'subtitle').text = yaml_data['subtitle']
xml_etree.SubElement(channel_element, 'itunes:author').text = yaml_data['author']
xml_etree.SubElement(channel_element, 'description').text = yaml_data['description']
xml_etree.SubElement(channel_element, 'itunes:image', {'href': link_prefix + yaml_data['image']})
xml_etree.SubElement(channel_element, 'language').text = yaml_data['language']
xml_etree.SubElement(channel_element, 'link').text = link_prefix

xml_etree.SubElement(channel_element, 'itunes:category', {'text': yaml_data['category']})

for item in yaml_data['item']:
    item_element = xml_etree.SubElement(channel_element, 'item')
    xml_etree.SubElement(item_element, 'title').text = item['title']
    xml_etree.SubElement(item_element, 'description').text = item['description']
    xml_etree.SubElement(item_element, 'pubDate').text = item['published']
    xml_etree.SubElement(item_element, 'itunes:duration').text = item['duration']
    xml_etree.SubElement(item_element, 'title').text = item['title']

    enclosure = xml_etree.SubElement(item_element, 'enclosure', {
       'url': link_prefix + item['file'], 
       'type': 'audio/mpeg',
       'length': item['length']
})

output_tree = xml_etree.ElementTree(rss_element)
output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)

