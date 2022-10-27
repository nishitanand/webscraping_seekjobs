# webscraping_seekjobs

nishit_webscraping_SeekJobs_main.py is the python program and on running it, it will do the scraping and save all the data in the list called mainlist

I have used conda on Ubuntu 20.04 for this task and have created a virtual environemnt using conda, which you can replicate using the yaml file and the command

conda env create -f nishit_seekjobs.yml

Note: Conda needs to be installed already for this

After this a virtual environment will be created using conda called nishit_seekjobs
Activate this environment using the command

conda activate nishit_seekjobs

Now the environment has been activated. Just run the python file using the command

python3 nishit_webscraping_SeekJobs_main.py

OR

python nishit_webscraping_SeekJobs_main.py

I have used only requests library and BeautifulSoup Library of Python, So if you install these 2 only (without installing conda and replicating the virtual environemnt), then also the python program would work. But the ideal condition for reproducibility is using conda

