def extract_skills(self, text: str) -> Set[str]:
    text_lower = text.lower()
    found_skills = set()

    for category, skills_dict in self.skills_taxonmy.items():
        for skill_name, variations in skills_dict.items():
            for variation in variations:
                # Prevent JavaScript from being detected as Java
                pattern = r"\\b" + re.escape(variation) + r"\\b"
                if re.search(pattern, text_lower):
                    found_skills.add(skill_name)
                    break  # No need to check other variations for this skill
    return found_skills
