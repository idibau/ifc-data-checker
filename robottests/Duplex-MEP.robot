*** Settings ***
Library    OperatingSystem
Library    Process

*** Variables ***
${rulesfile}       ./rulesfiles/duplex mep rules.yml
${ifcfile}         ./ifcfiles/Duplex-MEP.ifc
${expectedfile}    ./robottests/duplex-mep expected report.txt

*** Test Cases ***

predefined type
    ${result}=                     RUN PROCESS         python                   ifc_data_checker    ${rulesfile}    ${ifcfile}
    SHOULD BE EQUAL AS INTEGERS    ${result.rc}        0
    ${expectedvalidation}=         GET FILE            ${expectedfile}
    SHOULD BE EQUAL                ${result.stdout}    ${expectedvalidation}
