import collections
import re
import tensorflow as tf

def load_labelmap(path):
	# Minimal loader for pbtxt label map
	categories = []
	with open(path, 'r') as f:
		lines = f.readlines()
	item = {}
	for line in lines:
		if 'item' in line:
			item = {}
		if 'id:' in line:
			item['id'] = int(re.findall(r'id: (\d+)', line)[0])
		if 'name:' in line:
			match = re.search(r'name:\s*[\'\"](.+)[\'\"]', line)
			if match:
				item['name'] = match.group(1)
		if 'display_name:' in line:
			match = re.search(r'display_name:\s*[\'\"](.+)[\'\"]', line)
			if match:
				item['display_name'] = match.group(1)
		if '}' in line and item:
			categories.append(item)
			item = {}
	return categories

def convert_label_map_to_categories(label_map, max_num_classes=90, use_display_name=True):
	categories = []
	for item in label_map:
		if item['id'] <= max_num_classes:
			name = item.get('display_name') if use_display_name and 'display_name' in item else item['name']
			categories.append({'id': item['id'], 'name': name})
	return categories

def create_category_index(categories):
	category_index = {}
	for cat in categories:
		category_index[cat['id']] = cat
	return category_index
