#!/usr/bin/python
import subprocess
import sys
import time
import os

#STARTING KUBERNETES
def start():

	#Starting minikube
	subprocess.call("minikube start", shell = True)

	#Starting dashboard
	subprocess.call("minikube dashboard", shell = True)

	#Starting docker machine
	subprocess.call("docker-machine start default", shell = True)
	subprocess.call("docker-machine env default", shell = True)



#CREATING PROJECT
def create():

	#Creating dockerfile
	file=open("prueba", "w")
	file.write("FROM ubuntu:14.04\n")
	file.write("RUN sudo apt-get update\n")
	file.write("RUN sudo apt-get install curl -y\n")
	file.write("RUN sudo curl -sL https://deb.nodesource.com/setup_7.x | sudo bash -\n")
	file.write("RUN sudo apt-get install nodejs -y\n")
	file.write("RUN sudo apt-get install git -y\n")
	file.write("RUN git clone https://github.com/CORE-UPM/CRM_2017\n")
	file.write("WORKDIR CRM_2017\n")
	file.write("RUN sudo npm install\n")
	file.write("RUN sudo npm run-script migrate_local\n")
	file.write("RUN sudo npm run-script seed_local\n")
	file.write("EXPOSE 3000\n")
	file.write("CMD sudo npm run-script supervisor")
	file.close

	#Build dockerfile
	subprocess.call("docker build --rm=true -t crm .", shell = True)

	#Pushing repository at docker hub
	subprocess.call("docker tag crm danielmartingarcia/crm", shell = True)
	subprocess.call("docker push danielmartingarcia/crm")

	#Run image
	subprocess.call("kubectl run crm --image=danielmartingarcia/crm --port=3000", shell = True)
	subprocess.call("kubectl expose deployment crm --type=NodePort", shell = True)



#LAUNCH PROJECT
def launch():
	#Launching browser
	subprocess.call("minikube service crm", shell = True)



#DELETING IMAGES, PODS AND SERVICES
def delete():

	#Deleting service and deployment
	subprocess.call("kubectl delete service crm", shell = True)
	subprocess.call("kubectl delete deployment crm", shell = True)



#STOPPING KUBERNETES
def stop():

	#Stopping minikube
	subprocess.call("minikube stop", shell = True)

	#Stopping docker machine
	subprocess.call("docker-machine stop default", shell = True)



#CHECKING ARGUMENTS WHEN LAUNCHING THE SCRIPT

#Checking the status of minikube
status = subprocess.run("minikube status", stdout=subprocess.PIPE).stdout.decode('utf-8')

#When passing no arguments
if len(sys.argv) < 2:
	exit("Error: you have to write an argument")

#When passing an argument
else:
	#When argument is "start"
	if sys.argv[1] == "start":
		if status == "minikube: Stopped\ncluster: \nkubectl: \n":
			start()
			exit("Minikube started")
		else:
			exit("Error: kubernetes already started")

	#When argument is "create"
	elif sys.argv[1] == "create":
		if status == "minikube: Stopped\ncluster: \nkubectl: \n":
			create()
			exit("Project created")
		else:
			exit("Error: can't create because minikube is stopped. To start minikube, use argument 'create'")


	#When argument is "stop"
	elif sys.argv[1] == "stop":
		if status == "minikube: Stopped\ncluster: \nkubectl: \n":
			exit("Error: minikube is already stopped")
		else:
			stop()
			exit("Minikube stopped")

	#When argument is "delete"
	elif sys.argv[1] == "delete":
		if status == "minikube: Stopped\ncluster: \nkubectl: \n":
			exit("Error: minikube is already stopped and can't delete project")
		else:
			stop()
			exit("Project destroyed")
	else:
		exit("Error: invalid argument")