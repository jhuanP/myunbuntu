#!/bin/bash

 

#this will access ocp for you I had a lot of fun making took me a while hope you enjoy.

#for login to work you need to create a .password and .username file with your creds

 

echo "Would you like Prod1/2 or Mod envs?"

 

read modOrProd

 

case $modOrProd in

"Prod1") echo "Using Prod1";;

"Prod2") echo "Using Prod2";;

"prod1") echo "Using Prod1";;

"prod2") echo "Using Prod2";;

"p1") echo "Using Prod1";;

"p2") echo "Using Prod2";;

"Mod") echo "Using Mod";;

"mod") echo "Using Mod";;

"m") echo "Using Mod";;

*) echo "Sorry that is not an available environment please try again"

   ./oc-guruish.sh;;

esac

 

if [ $modOrProd = "Mod" ] || [ $modOrProd = "mod" ] || [ $modOrProd = "m" ]

  then

    echo "Which environment would you like to use? DEV(d)/QA(q)/CAP(c)"

 

    read env

 

    case $env in

    "DEV") echo "thats Dev correct?";;

    "dev") echo "thats Dev correct?";;

    "d") echo "thats Dev correct?";;

    "QA") echo "thats QA correct?";;

    "qa") echo "thats QA correct?";;

    "q") echo "thats QA correct?";;

    "CAP") echo "thats CAP correct?";;

    "cap") echo "thats CAP correct?";;

    "c") echo "thats CAP correct?";;

    *) echo "Sorry that is not an available environment please try again"

       ./oc-guruish.sh;;

    esac

 

  read ans

 

  if [ $ans = "yes" ] || [ $ans = "YES" ] || [ $ans = "y" ]

    then

      if [ $env = "DEV" ] || [ $env = "dev" ] || [ $env = "d" ]

        then

          env="dev"

          oc login https://master.ocp-dev(domain).com:443 -u=$(<.username.txt) -p=$(<.password.txt)

 

      elif [ $env = "QA" ] || [ $env = "qa" ] || [ $env = "q" ]

        then

          env="qa"

          oc login https://master.ocp-qa.(domain).com:443 -u=$(<.username.txt) -p=$(<.password.txt)

 

      elif [ $env = "CAP" ] || [ $env = "cap" ] || [ $env = "c" ]

        then

          env="cap"

          oc login https://master.ocp-cap(domain).com:443 -u=$(<.username.txt) -p=$(<.password.txt)

        fi

  else

    echo "please select correct environment"

    ./oc-guruish.sh

    fi

 

echo "Do you know the project you need? (leave blank to skip)"

 

  read project

 

  case $project in

  "yes") echo "What project do you need?"

         read need

         oc project $need;;

  "no") echo "Here are the projects"

        oc get projects | awk 'NR == 1 {next} {print $1}'

        ./oc-guruish.sh ;;

  *) echo "Sorry that is not an available option, step skipped";;

  esac

 

  echo "Would you like to pull routes?"

 

  read routes

 

  if [ $routes = "Yes" ] || [ $routes = "y" ] || [ $routes = "yes" ]

    then

      timestamp="$(date +'%Y%m%d-%H%M%S')"

      urllist= oc get routes | awk 'NR == 1 {next} {print $2}' > url.txt

 

      while read url

      do

      echo "https://$url"  >> ocp-routes-$env-$timestamp.txt

      done < url.txt

 

      rm url.txt

 

  elif [ $routes = "No" ] || [ $routes = "n" ] || [ $routes = "no" ]

      then

        echo "Ok will not create document of routes"

  else

    echo "Sorry I did not understand but you're still logged in :)"

    fi

    exit

 

elif [ $modOrProd = "Prod1" ] || [ $modOrProd = "prod1" ] || [ $modOrProd = "Prod2" ] || [ $modOrProd = "prod2" ] || [ $modOrProd = "p1" ] || [ $modOrProd = "p2" ]

    then

      if [ $modOrProd = "Prod1" ] || [ $modOrProd = "prod1" ] || [ $modOrProd = "p1" ]

        then

          modOrProd="prod1"

          oc login https://master.ocp-$modOrProd.(domain).com:443 -u=$(<.username.txt) -p=$(<.password.txt)

 

      elif [ $modOrProd = "Prod2" ] || [ $modOrProd = "prod2" ] || [ $modOrProd = "p2" ]

        then

          modOrProd="prod2"

          oc login https://master.ocp-$modOrProd.(domain).com:443 -u=$(<.username.txt) -p=$(<.password.txt)

        fi

else

  echo "Please choose Mod or Prod1/Prod2 you can even type m or p1 or p2 "

  ./oc-guruish.sh

  fi

 

echo "Do you know the project you need? (leave blank to skip)"

 

read project

 

case $project in

  "yes") echo "What project do you need?"

         read need

        oc project $need;;

  "no") echo "Here are the projects"

        oc get projects | awk 'NR == 1 {next} {print $1}'

        ./oc-guruish.sh;;

  *) echo "Sorry that is not an available option step skipped";;

esac

 

echo "Would you like to pull routes?"

 

read routes

 

  if [ $routes = "Yes" ] || [ $routes = "y" ] || [ $routes = "yes" ]

    then

      timestamp="$(date +'%Y%m%d-%H%M%S')"

      urllist= oc get routes | awk 'NR == 1 {next} {print $2}' > url.txt

      while read url

      do

      echo "https://$url"  >> ocp-routes-$modOrProd-$timestamp.txt

      done < url.txt

 

      rm url.txt

      echo "Done, type ls and look for ocp-routes* to see routes"

  elif [ $routes = "No" ] || [ $routes = "n" ] || [ $routes = "no" ]

    then

      echo "Ok will not create document of routes"

  else

      echo "Sorry I did not understand but you're still logged in :)"

    fi
