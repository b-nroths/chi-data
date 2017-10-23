datas = {
	"bloomberg": {
		"title": "Bloomberg",
		"definition": "Number of articles in Bloomberg",
		"categories": ["News"],
		"reports": ["Articles", "311"],
		"group_by": False,
		"goal": 50,
		"current": True,
		"query": """
			SELECT CAST(published_at AS DATE), COUNT(*)
			FROM articles.article
			WHERE
				site = 'bloomberg'
			GROUP BY 1
		""",
		"query_current": """
			SELECT CAST(date_part('HOUR', published_at) AS INT), COUNT(*)
			FROM articles.article
			WHERE
				CAST(published_at AS DATE) IN (
					current_date - 7,
					current_date - 14,
					current_date - 21,
					current_date - 28) AND
					site = 'bloomberg'
			GROUP BY 1
			ORDER BY 1
		"""
	},
	"the-new-york-times": {
		"title": "NY Times",
		"definition": "Number of Articles in the New York Times",
		"categories": ["News"],
		"reports": ["Articles", "Crime"],
		"group_by": False,
		"goal": 50,
		"current": True,
		"query": """
			SELECT CAST(published_at AS DATE), COUNT(*)
			FROM articles.article
			WHERE
				site = 'the-new-york-times'
			GROUP BY 1
		""",
		"query_current": """
			SELECT CAST(date_part('HOUR', published_at) AS INT), COUNT(*)
			FROM articles.article
			WHERE
				CAST(published_at AS DATE) IN (
					current_date - 7,
					current_date - 14,
					current_date - 21,
					current_date - 28) AND
					site = 'the-new-york-times'
			GROUP BY 1
			ORDER BY 1
		"""
	},
	"hacker-news": {
		"title": "Hacker News",
		"definition": "Number of articles in Hacker News",
		"categories": ["News"],
		"reports": ["Articles"],
		"group_by": False,
		"goal": 50,
		"current": True,
		"query": """
			SELECT CAST(published_at AS DATE), COUNT(*)
			FROM articles.article
			WHERE
				site = 'hacker-news'
			GROUP BY 1
		""",
		"query_current": """
			SELECT CAST(date_part('HOUR', published_at) AS INT), COUNT(*)
			FROM articles.article
			WHERE
				CAST(published_at AS DATE) IN (
					current_date - 7,
					current_date - 14,
					current_date - 21,
					current_date - 28) AND
					site = 'hacker-news'
			GROUP BY 1
			ORDER BY 1
		"""
	},
	"daily-mail": {
		"title": "Daily Mail",
		"definition": "Number of articles in Daily Mail",
		"categories": ["News"],
		"reports": ["Articles"],
		"group_by": False,
		"goal": 50,
		"current": True,
		"query": """
			SELECT CAST(published_at AS DATE), COUNT(*)
			FROM articles.article
			WHERE
				site = 'daily-mail'
			GROUP BY 1
		""",
		"query_current": """
			SELECT CAST(date_part('HOUR', published_at) AS INT), COUNT(*)
			FROM articles.article
			WHERE
				CAST(published_at AS DATE) IN (
					current_date - 7,
					current_date - 14,
					current_date - 21,
					current_date - 28) AND
					site = 'daily-mail'
			GROUP BY 1
			ORDER BY 1
		"""
	},
	"metro": {
		"title": "Metro",
		"definition": "Number of articles in Metro",
		"categories": ["News"],
		"reports": ["Articles"],
		"group_by": False,
		"goal": 50,
		"current": True,
		"query": """
			SELECT CAST(published_at AS DATE), COUNT(*)
			FROM articles.article
			WHERE
				site = 'metro'
			GROUP BY 1
		""",
		"query_current": """
			SELECT CAST(date_part('HOUR', published_at) AS INT), COUNT(*)
			FROM articles.article
			WHERE
				CAST(published_at AS DATE) IN (
					current_date - 7,
					current_date - 14,
					current_date - 21,
					current_date - 28) AND
					site = 'metro'
			GROUP BY 1
			ORDER BY 1
		"""
	},
	"business-insider": {
		"title": "Business Insider",
		"definition": "Number of articles in Business Insider",
		"categories": ["News"],
		"reports": ["Articles"],
		"group_by": False,
		"goal": 50,
		"current": True,
		"query": """
			SELECT CAST(published_at AS DATE), COUNT(*)
			FROM articles.article
			WHERE
				site = 'business-insider'
			GROUP BY 1
		""",
		"query_current": """
			SELECT CAST(date_part('HOUR', published_at) AS INT), COUNT(*)
			FROM articles.article
			WHERE
				CAST(published_at AS DATE) IN (
					current_date - 7,
					current_date - 14,
					current_date - 21,
					current_date - 28) AND
					site = 'business-insider'
			GROUP BY 1
			ORDER BY 1
		"""
	},
	"crimes": {
		"title": "Crimes",
		"definition": "The crimes",
		"categories": ["Crime"],
		"reports": ["Crime"],
		"group_by": False,
		"goal": 50,
		"current": False,
		"query": """
			SELECT CAST(dt AS DATE), COUNT(*)
			FROM datasets.crimes
			GROUP BY 1
		""",
		"query_current": None
	},
	"murders": {
		"title": "Murders",
		"definition": "The murders",
		"categories": ["Crime"],
		"reports": ["Crime"],
		"goal": 50,
		"current": False,
		"group_by": False,
		"query": """
			SELECT CAST(dt AS DATE), COUNT(*)
			FROM datasets.crimes
			WHERE 
				json_data::json->>'description' = 'FIRST DEGREE MURDER'
			GROUP BY 1
		""",
		"query_current": None
	},
	"alley_lights_out_311": {
		"title": "Alley Lights Out",
		"definition": "The murders",
		"categories": ["311"],
		"reports": ["Crime"],
		"goal": 50,
		"current": False,
		"group_by": False,
		"query": """
			SELECT CAST(dt AS DATE), COUNT(*)
			FROM datasets.alley_lights_out_311
			GROUP BY 1
		""",
		"query_current": None
	},
	"building_violations": {
		"title": "Building Violations",
		"definition": "The murders",
		"categories": [],
		"reports": [],
		"goal": 50,
		"current": False,
		"group_by": False,
		"query": """
			SELECT CAST(dt AS DATE), COUNT(*)
			FROM datasets.building_violations
			GROUP BY 1
		""",
		"query_current": None
	},
	"food_inspections": {
		"title": "Food Inspections",
		"definition": "The murders",
		"categories": [],
		"reports": [],
		"goal": 50,
		"current": False,
		"group_by": False,
		"query": """
			SELECT CAST(dt AS DATE), COUNT(*)
			FROM datasets.food_inspections
			GROUP BY 1
		""",
		"query_current": None
	},
	"graffiti_311": {
		"title": "Graffiti",
		"definition": "The murders",
		"categories": ["311"],
		"reports": ["311"],
		"goal": 50,
		"current": False,
		"group_by": False,
		"query": """
			SELECT CAST(dt AS DATE), COUNT(*)
			FROM datasets.graffiti_311
			GROUP BY 1
		""",
		"query_current": None
	},
	"sanitation_311": {
		"title": "Sanitation",
		"definition": "The murders",
		"categories": ["311"],
		"reports": ["311"],
		"goal": 50,
		"current": False,
		"group_by": False,
		"query": """
			SELECT CAST(dt AS DATE), COUNT(*)
			FROM datasets.sanitation_311
			GROUP BY 1
		""",
		"query_current": None
	},
	"vacant_311": {
		"title": "Vacant",
		"definition": "The murders",
		"categories": ["311"],
		"reports": ["311"],
		"goal": 50,
		"current": False,
		"group_by": False,
		"query": """
			SELECT CAST(dt AS DATE), COUNT(*)
			FROM datasets.vacant_311
			GROUP BY 1
		""",
		"query_current": None
	}
}