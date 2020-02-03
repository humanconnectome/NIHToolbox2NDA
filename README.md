# NIHToolbox2NDA
collection of python3 commands and a couple of useful functions in a jupyter notebox which can be used to reformat NIH Toolbox data (as csv exports of Scores and Raw data from an iPad application) into NDA structures

Besides setting up the environment with the requirements.txt file, you'll need to prepare four files.

Two are in the .csv format of the IPAD Toolbox applcation export. E.g. a raw Data file containing item level responses, and a Scores file, containing the summary statistics for the collection of item level data. We don't need the registration file. These two files are linked by PIN and Inst variables, and must be cleaned a priori, to remove subjects that are in one but not the other file. I.e. the list of unique PINs (ex. HCP0211999_V1) in one file should be exactly the same as the list of unique PINs in the other. For HCP data, we concatenate the exports of all subjects' Score data in to a single file, and the exports of all subjects Raw data into a second file. Because all other sources of HCP data use 'subject' and 'visit' rather than a PIN which is a concatenation of both, we create these variables (subject and visit) from PIN prior to running this program as well.

The third necessary file is a csv containing the fields that NDA requires in all of their structures e.g. subjectkey (GUID or pseudo-GUID), src_subject_id (e.g. HCP0211999), interview_age (in months), and gender (misnomer for sex assigned at birth). In HCP data, we link the two sources of information via 'subject' and 'visit.'

Lastly, a crosswalk file - this will map your vars to NDA after transpose is complete. I have placed the crosswalk from HCPA as an example. Any instruments in this crosswalk that are the same as yours (look at 'Inst' column) will work for you. You will have to add any instruments not present, after obtaining variable maps and templates from the NDA for your particular set of NIH Toolbox Data.  If you get these maps and templates from the NDA in the form of several (dozen) zipped directories, you can use crosswalkscratch.py in this repository to facilitate the transformation of NDA requests into a centralzied crosswalk.

Description of variables in the crosswalk: 
Inst = NIH Toolbox Instrument Name - e.g. the contents of 'Inst' 

hcp_variable =	Name of the Variable being mapped, as it exists in HCP data ready for crossing over - note that for NIH Toolbox Data, HCP Variables are not ready until spaces and special characters have been replaced with underscores

nda_structure =	NDA Structure to which our data is mapped

nda_element =	NDA Element to which our data is mapped

inst_short =	NDAs shorthand for NIH Toolbox Instrument  - this is NOT NDAs name for any particular structure -  it is merely used in crossover mapping - was the name of the unzipped folder that we received with all the mapping information for a particular instrument.

template - name of NDA template provided by Leo for crossover mapping

action_request -	Requests that NDA made of CCF to avoid naming conflicts, or value codings, etc. 

hcp_variable_upload -	HCP Variable name in uploaded file (usually the same as HCP_Variable because NDA took care of the mapping to NDA_Element, but some cases required renames to avoid conflict

requested_python -	Python code to handle Form Requests, unless specialty code required

specialty_code -	Indicator variable for whether form request requires code that cant be handled with a handful of Python statements in the requested_python column.  >=0 means solution required special consideration in crosswalk.py
