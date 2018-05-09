import utils
from os.path import isfile


def populate_concept_level_performance(complete_validation_file, c_map_file):
    if isfile(c_map_file):
        return utils.load_json_data(c_map_file)
    lines = utils.read_text_file(complete_validation_file)
    concept2label = {}
    for l in lines[1:]:
        arr = l.split('\n')
        label = arr[2]
        concept = arr[8]
        c_map = None
        if concept in concept2label:
            c_map = {}
            concept2label[concept] = c_map
        else:
            c_map = concept2label[concept]
        if label in c_map:
            c_map[label] = 1
        else:
            c_map[label] += 1
    utils.save_json_array(c_map, c_map_file)
    return c_map


def populate_phenotype_validation_results(phenotype_def_file,
                                          complete_validation_file, c_map_file,
                                          output_file):
    c_map = populate_concept_level_performance(complete_validation_file, c_map_file)
    phenotypes = utils.load_json_data(phenotype_def_file)
    for p in phenotypes:
        p['validation'] = {}
        for c in phenotypes[p]['concepts']:
            for label in c_map[c]:
                if label in p['validation']:
                    p['validation'][label] += c_map[label]
                else:
                    p['validation'][label] = c_map[label]
    utils.save_json_array(phenotypes, output_file)
    print 'done'


if __name__ == "__main__":
    populate_phenotype_validation_results('./data/phenotype_def_file',
                                          './data/compelete_validat_file',
                                          './data/c_map_file.json', './data/phenotype_def_with_validation.json')