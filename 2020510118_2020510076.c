#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <arpa/inet.h>
#include <libxml/parser.h>
#include <libxml/tree.h>
#include <libxml/xmlschemastypes.h>
#define RECORD_COUNT 50

struct _Person
{
    char name[20];
    char surname[30];
    char gender[2];
    char occupancy[30];
    char level_of_education[4];
    char email[50];
    char bank_account_number[13];
    char iban[28];
    char account_type[14];
    char currency_unit[5];
    char total_balance_available[5];
    char available_for_loan[4];
};

typedef struct _Person Person;
Person wItem, rItem;

void csv_To_Binary(char srcFile[], char destFile[])
{
    FILE *the_file = fopen(srcFile, "r");
    if (the_file == NULL)
    {
        perror("Unable to open the file.");
        exit(1);
    }

    FILE *fp;
    fp = fopen(destFile, "w"); // open a stream with r, w, a modes
    if (fp == NULL)
    {
        puts("error opening file!");
        exit(1);
    }

    char line[200];

    // skips the first line
    bool flag = true;
    while (flag && fgets(line, sizeof(line), the_file))
    {
        char *a;
        a = strtok(line, ",");
        while (a != NULL)
        {
            a = strtok(NULL, ",");
        }
        flag = false;
    }

    // read each line of the csv data
    while (fgets(line, sizeof(line), the_file))
    {
        char *token;
        token = strtok(line, ","); // splitting the current line with respect to comma
        while (token != NULL)
        {
            // these conditions are for placing the data into correct struct

            // name
            if (strlen(token) <= 20) // condition for placing the data correctly
            {
                strcpy(wItem.name, token);                     // copies token into wItem
                fwrite(wItem.name, sizeof(wItem.name), 1, fp); // gets a place as the size of name struct and writes name into binary file
                token = strtok(NULL, ",");                     // gets the next data
            }

            // surname
            if (strlen(token) <= 30) // condition for placing the data correctly
            {
                strcpy(wItem.surname, token);
                fwrite(wItem.surname, sizeof(wItem.surname), 1, fp);
                token = strtok(NULL, ",");
            }

            // gender
            if (strcmp(token, "F") == 0 || strcmp(token, "M") == 0) // controls if gender data is either "F" or "M"
            {
                strcpy(wItem.gender, token);
                fwrite(wItem.gender, sizeof(wItem.gender), 1, fp);
                token = strtok(NULL, ",");
            }

            // occupancy
            if (strlen(token) > 3 && strlen(token) <= 30) // for not placing the level_of_education struct into occupancy struct if the occupancy is empty
            {
                strcpy(wItem.occupancy, token);
                fwrite(wItem.occupancy, sizeof(wItem.occupancy), 1, fp);
                token = strtok(NULL, ",");
            }
            else // if the occupancy is empty, write "invalid occupancy" into occupancy struct
            {
                strcpy(wItem.occupancy, " ");
                fwrite(wItem.occupancy, sizeof(wItem.occupancy), 1, fp);
            }

            // level_of_education
            // checks if the level of education is in correct format
            if (strcmp(token, "PS") == 0 || strcmp(token, "HS") == 0 || strcmp(token, "BSc") == 0 || strcmp(token, "MSc") == 0 || strcmp(token, "PhD") == 0)
            {
                strcpy(wItem.level_of_education, token);
                fwrite(wItem.level_of_education, sizeof(wItem.level_of_education), 1, fp);
                token = strtok(NULL, ",");
            }

            // email
            char *ret;
            const char ch = '@';
            ret = strchr(token, ch); // gets the substring of the token that starts with "@"

            if (ret == NULL) // if email is empty, writes "invalid email"
            {
                strcpy(wItem.email, " ");
                fwrite(wItem.email, sizeof(wItem.email), 1, fp);
                // there is no strtok, because the current token is bank account number
            }
            else if (strcmp(ret, "@gmail.com") == 0 || strcmp(ret, "@hotmail.com") == 0 || strcmp(ret, "@yahoo.com") == 0) // if email is in correct form
            {
                strcpy(wItem.email, token);
                fwrite(wItem.email, sizeof(wItem.email), 1, fp);
                token = strtok(NULL, ",");
            }
            else // if email form is wrong (i.e. @emre.com, @duru.com), writes "invalid email"
            {
                strcpy(wItem.email, " ");
                fwrite(wItem.email, sizeof(wItem.email), 1, fp);
                token = strtok(NULL, ",");
            }

            // bank account number
            strcpy(wItem.bank_account_number, token);
            fwrite(wItem.bank_account_number, sizeof(wItem.bank_account_number), 1, fp);
            token = strtok(NULL, ",");

            // IBAN
            strcpy(wItem.iban, token);
            fwrite(wItem.iban, sizeof(wItem.iban), 1, fp);
            token = strtok(NULL, ",");

            // account type
            strcpy(wItem.account_type, token);
            fwrite(wItem.account_type, sizeof(wItem.account_type), 1, fp);
            token = strtok(NULL, ",");

            // currency unit
            strcpy(wItem.currency_unit, token);
            fwrite(wItem.currency_unit, sizeof(wItem.currency_unit), 1, fp);
            token = strtok(NULL, ",");

            // total balance available
            strcpy(wItem.total_balance_available, token);
            fwrite(wItem.total_balance_available, sizeof(wItem.total_balance_available), 1, fp);
            token = strtok(NULL, ",");

            // available for loan
            // adding the emoji to struct and binary file according to emoji's size
            char *a;
            a = strtok(token, "\n");
            strcpy(wItem.available_for_loan, a);
            fwrite(wItem.available_for_loan, sizeof(wItem.available_for_loan), 1, fp);
            token = strtok(NULL, ",");
        }
    }

    fclose(the_file);
    fclose(fp);
}

void binary_To_XML(char srcFile[], char destFile[])
{
    FILE *fp;
    fp = fopen(srcFile, "r");
    if (fp == NULL)
    {
        printf("Error opening file!");
        exit(1);
    }

    xmlDocPtr doc = NULL;                                                                        /* document pointer */
    xmlNodePtr root_node = NULL, row = NULL, customer = NULL, bank_account = NULL, total = NULL; /* node pointers */
    int i, j;

    /*
     * Creates a new document, a node and set it as a root node
     */
    doc = xmlNewDoc(BAD_CAST "1.0");
    root_node = xmlNewNode(NULL, BAD_CAST "records"); // creates node as "records"
    xmlDocSetRootElement(doc, root_node);             // sets root element
    char version_str[2], bigEndian_str[16];

    for (i = 0; i < RECORD_COUNT; i++)
    {
        fread(&rItem, sizeof(Person), 1, fp);                     // read the binary file as the size of Person struct
        row = xmlNewChild(root_node, NULL, BAD_CAST "row", NULL); // creates root node's child
        sprintf(version_str, "%d", i + 1);                        // not to write to a file or screen but to write the int id number as char array
        xmlNewProp(row, BAD_CAST "id", BAD_CAST version_str);     // creates new "id" property into the row

        customer = xmlNewChild(row, NULL, BAD_CAST "customer_info", NULL);                             // creates row node's child "customer_info"
        xmlNewChild(customer, NULL, BAD_CAST "name", BAD_CAST rItem.name);                             // creates customer_info node's child "name"
        xmlNewChild(customer, NULL, BAD_CAST "surname", BAD_CAST rItem.surname);                       // creates customer_info node's child "surname"
        xmlNewChild(customer, NULL, BAD_CAST "gender", BAD_CAST rItem.gender);                         // creates customer_info node's child "gender"
        xmlNewChild(customer, NULL, BAD_CAST "occupancy", BAD_CAST rItem.occupancy);                   // creates customer_info node's child "occupancy"
        xmlNewChild(customer, NULL, BAD_CAST "level_of_education", BAD_CAST rItem.level_of_education); // creates customer_info node's child "level_of_education"
        xmlNewChild(customer, NULL, BAD_CAST "email", BAD_CAST rItem.email);                           // creates customer_info node's child "email"

        bank_account = xmlNewChild(row, NULL, BAD_CAST "bank_account_info", NULL);                                           // creates row node's child "bank_account_info"
        xmlNewChild(bank_account, NULL, BAD_CAST "bank_account_number", BAD_CAST rItem.bank_account_number);                 // creates bank_account_info node's child "bank_account_number"
        xmlNewChild(bank_account, NULL, BAD_CAST "IBAN", BAD_CAST rItem.iban);                                               // creates bank_account_info node's child "IBAN"
        xmlNewChild(bank_account, NULL, BAD_CAST "account_type", BAD_CAST rItem.account_type);                               // creates bank_account_info node's child "account_type"
        total = xmlNewChild(bank_account, NULL, BAD_CAST "total_balance_available", BAD_CAST rItem.total_balance_available); // creates bank_account node's child "total_balance_available"
        xmlNewProp(total, BAD_CAST "currency_unit", BAD_CAST rItem.currency_unit);                                           // creates total_balance_available node's child "currency_unit"

        // Convert Little Endian to Big Endian
        int littleEndian_int = strtol(rItem.total_balance_available, NULL, 10);                            // convert char to int
        int bigEndian_int = htonl(littleEndian_int);                                                       // htonl func. converts to binary and reads backwards
        sprintf(bigEndian_str, "%d", bigEndian_int);                                                       // casting
        xmlNewProp(total, BAD_CAST "bigEnd_Version", BAD_CAST bigEndian_str);                              // creates new "bigEnd_Version" property into the total_balance_available
        xmlNewChild(bank_account, NULL, BAD_CAST "available_for_loan", BAD_CAST rItem.available_for_loan); // creates bank_account_info node's child "available_for_loan"
    }
    fclose(fp);
    xmlSaveFormatFileEnc(destFile, doc, "UTF-8", 1);
    xmlSaveFormatFileEnc("-", doc, "UTF-8", 1);
    // xmlSaveFormatFile
    /*free the document */
    xmlFreeDoc(doc);
    /*
     *Free the global variables that may
     *have been allocated by the parser.
     */
    xmlCleanupParser();
}

void XML_To_XSD(char srcFile[], char destFile[])
{
    xmlDocPtr doc;
    xmlSchemaPtr schema = NULL;
    xmlSchemaParserCtxtPtr ctxt;

    char *XMLFileName = srcFile; // write your xml file here
    char *XSDFileName = destFile; // write your xsd file here

    xmlLineNumbersDefault(1);                   // set line numbers, 0> no substitution, 1>substitution
    ctxt = xmlSchemaNewParserCtxt(XSDFileName); // create an xml schemas parse context
    schema = xmlSchemaParse(ctxt);              // parse a schema definition resource and build an internal XML schema
    xmlSchemaFreeParserCtxt(ctxt);              // free the resources associated to the schema parser context

    doc = xmlReadFile(XMLFileName, NULL, 0); // parse an XML file
    if (doc == NULL)
    {
        fprintf(stderr, "Could not parse %s\n", XMLFileName);
    }
    else
    {
        xmlSchemaValidCtxtPtr ctxt; // structure xmlSchemaValidCtxt, not public by API
        int ret;

        ctxt = xmlSchemaNewValidCtxt(schema);  // create an xml schemas validation context
        ret = xmlSchemaValidateDoc(ctxt, doc); // validate a document tree in memory
        if (ret == 0)                          // validated
        {
            printf("%s validates\n", XMLFileName);
        }
        else if (ret > 0) // positive error code number
        {
            printf("%s fails to validate\n", XMLFileName);
        }
        else // internal or API error
        {
            printf("%s validation generated an internal error\n", XMLFileName);
        }
        xmlSchemaFreeValidCtxt(ctxt); // free the resources associated to the schema validation context
        xmlFreeDoc(doc);
    }
    // free the resource
    if (schema != NULL)
        xmlSchemaFree(schema); // deallocate a schema structure

    xmlSchemaCleanupTypes(); // cleanup the default xml schemas types library
    xmlCleanupParser();      // cleans memory allocated by the library itself
    xmlMemoryDump();         // memory dump
}

void selectType(char srcFile[], char destFile[], int type) // for select run type
{
    if (type == 1) // convert csv to binary
    {
        csv_To_Binary(srcFile, destFile);
    }
    else if (type == 2) // convert binary to xml
    {
        binary_To_XML(srcFile, destFile);
    }
    else if (type == 3) // convert xml to xsd
    {
        XML_To_XSD(srcFile, destFile);
    }
    else
    {
        printf("invalid type");
    }
}

int main(int argc, char *argv[])
{

    selectType(argv[1], argv[2], atoi(argv[3]));
    return 0;
}