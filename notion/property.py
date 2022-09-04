class PagePropertyParser:
    def parse_title(self, property):
        return property['title'][0]['plain_text']

    def parse_rich_text(self, property):
        return ''.join([content['plain_text'] for content in property['rich_text']])
    
    def parse_select(self, property):
        return property['select']['name']
    
    def parse_date(self, property):
        return property['date']['start']
    
    def parse_created_time(self, property):
        return property['created_time']
    
    def parse_checkbox(self, property):
        return property['checkbox']
    
    def parse_properties(self, properties):
        result = {}
        for key, value in properties.items():
            if 'title' in value:
                result[key] = self.parse_title(value)
            elif 'rich_text' in value:
                result[key] = self.parse_rich_text(value)
            elif 'select' in value:
                result[key] = self.parse_select(value)
            elif 'date' in value:
                result[key] = self.parse_date(value)
            elif 'created_time' in value:
                result[key] = self.parse_created_time(value)
            elif 'checkbox' in value:
                result[key] = self.parse_checkbox(value)
        return result