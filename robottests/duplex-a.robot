*** Settings ***
Library    OperatingSystem
Library    Process

*** Variables ***
${rulesfile}       ./rulesfiles/duplex a rules.yml
${ifcfile}         ./ifcfiles/Duplex-A.ifc
${expectedfile}    ./robottests/duplex-a expected report.txt

*** Test Cases ***

Is Decomposed By and Has Material Associations
    ${result}=                     RUN PROCESS         python3                  ifc_data_checker    ${rulesfile}    ${ifcfile}    stdout=stdout.txt
    SHOULD BE EQUAL AS INTEGERS    ${result.rc}        0
    ${expectedvalidation}=         GET FILE            ${expectedfile}
    SHOULD BE EQUAL                ${result.stdout}    ${expectedvalidation}
