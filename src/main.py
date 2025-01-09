from adapter.xml.model_factory import ModelFactory
from utils.utils import get_input_file


if __name__ == '__main__':
    args = get_input_file()
    factory = ModelFactory()
    model = factory.xml_model_factory('uppaal')
    root = model.parse_xml(args.input_file)
    result = model.get_xml_data(root)
    model.print_dict(result)
