*** Settings ***
Library    OperatingSystem
Library    Process

*** Variables ***
${rulesfile}       ./rulesfiles/fzk haus rules.yml
${ifcfile}         ./ifcfiles/FZK-Haus.ifc
${expectedfile}    ./robottests/fzk-haus expected report.txt

*** Test Cases ***

property set and is typed by
    ${result}=                     RUN PROCESS         python                   ifc_data_checker    ${rulesfile}    ${ifcfile}
    LOG                            ${result.stderr}
    SHOULD BE EQUAL AS INTEGERS    ${result.rc}        0
    ${expectedvalidation}=         GET FILE            ${expectedfile}
    SHOULD BE EQUAL                ${result.stdout}    ${expectedvalidation}
