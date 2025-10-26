import spacy
from spacy.tokens import Doc
from typing import List, Dict, Set

class TravelNER:
    def __init__(self, model_name="en_core_web_md"):
        """Initialize spaCy with travel-specific entity extraction"""
        self.nlp = spacy.load(model_name)
        
        # Travel-specific keywords to enhance extraction
        self.travel_keywords = {
            'attractions': ['museum', 'park', 'temple', 'fort', 'palace', 'monument', 
                          'beach', 'market', 'bazaar', 'garden', 'zoo', 'aquarium'],
            'transport': ['station', 'airport', 'bus stand', 'metro', 'railway'],
            'accommodation': ['hotel', 'resort', 'hostel', 'guesthouse'],
            'food': ['restaurant', 'cafe', 'dhaba', 'food court', 'street food']
        }
        
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract travel-relevant entities from text
        
        Returns:
            Dict with categories: locations, attractions, organizations, misc
        """
        doc = self.nlp(text)
        
        entities = {
            'locations': [],
            'attractions': [],
            'organizations': [],
            'misc': []
        }
        
        # Extract spaCy entities
        for ent in doc.ents:
            entity_text = ent.text
            entity_label = ent.label_
            
            if entity_label in ['GPE', 'LOC']:  # Geo-political entity, Location
                entities['locations'].append(entity_text)
            elif entity_label == 'FAC':  # Facility
                entities['attractions'].append(entity_text)
            elif entity_label == 'ORG':  # Organization
                entities['organizations'].append(entity_text)
            else:
                entities['misc'].append(entity_text)
        
        # Enhance with travel keyword matching
        entities = self._enhance_with_keywords(text, entities)
        
        # Remove duplicates
        for key in entities:
            entities[key] = list(set(entities[key]))
        
        return entities
    
    def _enhance_with_keywords(self, text: str, entities: Dict) -> Dict:
        """Use travel keywords to find additional attractions"""
        text_lower = text.lower()
        
        for category, keywords in self.travel_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    # Extract noun phrases containing the keyword
                    doc = self.nlp(text)
                    for chunk in doc.noun_chunks:
                        if keyword in chunk.text.lower():
                            if category in ['attractions', 'transport', 'accommodation', 'food']:
                                entities['attractions'].append(chunk.text)
        
        return entities
    
    def extract_locations_for_maps(self, text: str) -> List[str]:
        """Extract location names suitable for Google Maps API queries"""
        entities = self.extract_entities(text)
        
        # Combine locations and attractions
        all_locations = entities['locations'] + entities['attractions']
        
        # Filter out very short or generic terms
        filtered = [loc for loc in all_locations if len(loc) > 3]
        
        return list(set(filtered))
