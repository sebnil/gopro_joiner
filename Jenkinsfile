#!groovy

// virtual environment should be unique per project
def venvName = "gopro_joiner"

pipeline {
    agent
    {
        label "Windows && Python"
    }

    stages {
        stage('Checkout') {
            steps {
                deleteDir()
                checkout scm
            }
        }

        stage('Create Virtual Environment')
        {
            steps {
                script {
                    // create a virtual environment to run code in
                    try {
                        bat "conda create --name ${venvName} python=3.6 --yes"
                    }
                    catch (Exception ex)
                    {
                        // don't care about environment creation failure, since it is most likely due to environment already being present
                    }
                }

                // update the environment
                bat "activate ${venvName} && conda update python"
            }
        }

        stage('Install requirements') {
            steps {
                // install all requirements listed in requirements.txt
                bat "activate ${venvName} && pip install -r requirements.txt"
            }
        }

        stage('Test') {
            steps {
                // run tests
                bat "activate ${venvName} && nosetests -w tests --with-xunit --verbosity=2"

                // publish test results
                junit 'nosetests.xml'
            }
        }

        stage('Static Code Analysis') {
            steps {
                // flake8 code analysis
                bat "activate ${venvName} && flake8 tests --exit-zero --output-file flake8.log"

                // pylint code analysis
                bat "activate ${venvName} && pylint tests --rcfile=./pylintrc > pylint.log | EXIT 0"

                // publish analysis from both flake8 and pylint
                step([$class: 'WarningsPublisher',
                    parserConfigurations: [
                        [
                            parserName: 'Pep8',
                            pattern: 'flake8.log'
                        ],
                        [
                            parserName: 'pylint',
                            pattern: 'pylint.log'
                        ]
                    ],
                ])
            }
        }
    }
}