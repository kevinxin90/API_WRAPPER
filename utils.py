import requests

headers = {'Accept': 'application/json'}

def dict_sweep(d, vals=[".", "-", "", "NA", "none", " ", "Not Available", "unknown"]):
    """
    @param d: a dictionary
    @param vals: a string or list of strings to sweep
    """
    for key, val in d.items():
        if val in vals:
            del d[key]
        elif isinstance(val, list):
            for item in val:
                if item in vals:
                    val.remove(item)
                elif isinstance(item, dict):
                    dict_sweep(item, vals)
            if len(val) == 0:
                del d[key]
        elif isinstance(val, dict):
            dict_sweep(val, vals)
            if len(val) == 0:
                del d[key]
    return d

def get_interaction_types():
	url = 'http://dgidb.genome.wustl.edu/api/v1/interaction_types.json'
	r = requests.get(url, headers=headers)
	return r.json()

def create_empty_dict(gene_id):
	interaction_types = get_interaction_types()
	new_dict = {gene_id: {}}
	for _interaction_type in interaction_types:
		new_dict[gene_id][_interaction_type] = []
	return new_dict

def transform_json(gene_id):
	url = 'http://dgidb.genome.wustl.edu/api/v1/interactions.json?genes=' + gene_id
	r = requests.get(url, headers=headers)
	interactions = r.json()["matchedTerms"][0]["interactions"]
	output_json = {'_id': gene_id}
	for _interaction in interactions:
		if _interaction['interactionType'] in output_json:
			output_json[_interaction['interactionType']].append(_interaction['drugName'])
		else:
			output_json[_interaction['interactionType']] = [_interaction['drugName']]
	return output_json