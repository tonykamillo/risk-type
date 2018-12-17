# Custom Risk Type

Proposal to allow insurers create their own risk types.
The approach consists in attach generic fields and values in order to define a risk, it's seems like a metadata tagging. There are three main models, one that holds the risk type itself and anothers two models hold field/value pair that going to be related to a risk type. For more details check it out the erd.png file.

# Data model
![ER diagram](https://drive.google.com/file/d/1IC7brOeUXLziyd_1rcJ1fwdofK3Knz79/view?usp=sharing)

# Deployment with zappa

 1. Clone this repo  `clone git@github.com:tonykamillo/risk-type.git`
 2. Create a virtualenv (assuming that you have a virtualenv installation in your machine)
     `virtualenv venv -p python2`
    It can be created inside risk-type folder. Python 2 intepreter was choosen because zappa only supports  2.7 to 3.6 versions.

 3. Activate the environment `source venv/bin/activate`
 4. Install dependencies `pip install -r requirements.txt`
 5. Inside risk-type folder create zappa initial settings `zappa init`
     Zappa wizard will ask you some informations, all of them should be answered.
 6. Into **zappa_settings.json** file add the option `"exclude":["*.sqlite3"]`
 7. Create a bucket for sqlite3 database `./manage.py createdb_s3bucket --settings britecore.settings.name_of_the_stage_environment`
    **IMPORTANT** For this step and the next is required make sure the aws crendentials, placed in your machine, has privilegies to manage following AWS Services: lambda, s3, cloud formation and api gateway.
 8. Deploy to AWS Lambda `zappa deploy name_of_the_stage_environment`
 9.  Execute `zappa manage name_of_the_stage_environment migrate` (just a doubling check if the database was created)
 10. Load sample data `zappa manage name_of_the_stage_environment "loaddata custom_risk_type/fixtures/initial_data.json"`
 11. Go to the address informed by zappa and start to create your own risk types, and then, create some insurances based on created risk type.


