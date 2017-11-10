# chi-data

## Data Integration Checklists
I'll check off a datasource once I have it continuously updating into AWS
### Data I have
- [X] http://plenar.io/explore/event/crimes_2001_to_present
- [X] http://plenar.io/explore/event/311_service_requests_graffiti_removal
- [X] http://plenar.io/explore/event/311_service_requests_vacant_and_abandoned_building
- [X] http://plenar.io/explore/event/311_service_requests_alley_lights_out
- [X] http://plenar.io/explore/event/311_service_requests_sanitation_code_complaints
- [X] http://plenar.io/explore/event/food_inspections
- [X] http://plenar.io/explore/event/business_licenses_current_liquor_and_public_places
- [X] http://plenar.io/explore/event/building_violations
- [X] Building Permits https://data.cityofchicago.org/Buildings/Building-Permits-Dashboard/2s3k-mec8

### NEXT UP
- [ ] LEHD Origin-Destination Employment Statistics (LODES) https://lehd.ces.census.gov/data/

### Additional Data
- [ ] https://usafacts.org/metrics/11699
- [ ] https://censusreporter.org/profiles/16000US1714000-chicago-il/
- [ ] https://www.zillow.com/research/data/ (1997)
- [ ] https://www.airdna.co/ (AirBnb)
- [ ] https://www.chicagocityscape.com/ building permit data (DUPLICATE)
- [ ] https://data.cityofchicago.org/browse?category=Health+%26+Human%20Services
- [ ] American Community Survey (census tracks)
- [ ] Radius, Google, YEXT, Yellow Pages
- [ ] Census of Businesses
- [ ] Quality of Life, longevity?
- [ ] twitter chicago
	- https://data.cityofchicago.org/Health-Human-Services/Public-Health-Statistics-Life-Expectancy-By-Commun/qjr3-bm53
	- https://www.cityofchicago.org/content/dam/city/depts/cdph/statistics_and_reports/LeadingCausesofDeathinChicago2007-2009.pdf
	- https://data.cityofchicago.org/Health-Human-Services/Public-Health-Statistics-Selected-underlying-cause/j6cj-r444
	- https://www.cdc.gov/nchs/data/nvsr/nvsr65/nvsr65_04.pdf
	- http://www.nber.org/data/vital-statistics-mortality-data-multiple-cause-of-death.html
	- http://www1.nyc.gov/assets/doh/downloads/pdf/epi/epiresearch-lifeexpectancy.pdf

### Related Research
- http://streetchange.media.mit.edu/

### Related Websites
- https://www.chicagocityscape.com/

### Interesting Blogs
- https://southsideweekly.com/
- https://southsidehealth.wordpress.com/
- http://www.uchospitals.edu/news/2012/20120508-communityrx.html

### Boundaries
- [ ] Census Blocks
- [ ] Community Areas
- [ ] Congressional Districts
- [ ] Empowerment Zones
- [ ] Neighborhoods
- [ ] Police Beats
- [ ] Police Districts
- [ ] State Congressional Districts
- [ ] State Senate Districts
- [ ] Tax Increment Financing Districts
- [ ] Ward Precincts
- [ ] Wards
- [ ] Zip Codes
- [ ] Schools
- [ ] Transport

## Folders
frontend/ (ReactJS published to AWS S3)
backend/ (Serverless published to AWS Lambda)

## Architecture
1. Cron Job on AWS ECS
2. Publish Data to S3 in Parquet
3. Read in pandas (or EMR) publish to DynamoDB
5. Serverless App on DynamoDB?

## Deploy
$ sh deploy.sh
url: http://chicago.bnroths.com