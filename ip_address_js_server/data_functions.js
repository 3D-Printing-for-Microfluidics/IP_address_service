printer_table = document.getElementById('printers');
device_table = document.getElementById('devices');

printer_header = document.getElementById('printers_header');
device_header = document.getElementById('devices_header');

function populateTable(table, header, is_printer, jsonObj) {

    var jsonName = "printer";
    if (!is_printer) {
        jsonName = "device";
    }

    var count = 0;

    for (const object in jsonObj) {
        count++;
    }

    //create header
    text = document.createElement('p');
    text.textContent = count + " " + jsonName + "(s) were found.";
    header.appendChild(text);

    //create table headers
    headerRow = document.createElement('tr');
    header1 = document.createElement('th');
    header2 = document.createElement('th');
    header3 = document.createElement('th');
    header4 = document.createElement('th');
    header5 = document.createElement('th');
    header6 = document.createElement('th');

    //add text to table headers
    header1.textContent = "Status"
    header2.textContent = "Host";
    header3.textContent = "IP Address";
    header4.textContent = "Port";
    header5.textContent = "Series";
    header6.textContent = "Version";

    //style borders
    header1.style.border = "1px solid #BBBBBB";
    header2.style.border = "1px solid #BBBBBB";
    header3.style.border = "1px solid #BBBBBB";
    header4.style.border = "1px solid #BBBBBB";
    header5.style.border = "1px solid #BBBBBB";
    header6.style.border = "1px solid #BBBBBB";

    //add table headers
    headerRow.appendChild(header1);
    headerRow.appendChild(header2);
    headerRow.appendChild(header3);
    if (is_printer) {
        headerRow.appendChild(header4);
    }
    headerRow.appendChild(header5);
    headerRow.appendChild(header6);
    table.appendChild(headerRow);

    //loop through all printer listings
    for (const object in jsonObj) {
        //create table columns
        row = document.createElement('tr');
        col1 = document.createElement('td');
        col2 = document.createElement('td');
        col3 = document.createElement('td');
        col4 = document.createElement('td');
        col5 = document.createElement('td');
        col6 = document.createElement('td');

        //get printer info
        temp = jsonObj[object];

        //create hyperlink
        a = document.createElement('a');
        link = document.createTextNode(temp.address);
        a.appendChild(link);
        a.title = temp.address;
        a.href = "http://" + temp.address + ":" + temp.port;

        //set printer status and icon
        var icon = document.createElement('span');
        if (temp.stat == 0) {
            col1.textContent = "Offline";
            icon.style = "font-size: 16px; color: Red; float:right;";
            icon.textContent = '\u2612';
        }
        else if (temp.stat == 1) {
            col1.textContent = "Server Offline";
            icon.style = "font-size: 18px; color: Orange; float:right;";
            icon.textContent = '\u2610';
        }
        else if (temp.stat == 2) {
            col1.textContent = "Online";
            icon.style = "font-size: 16px; color: Green; float:right;";
            icon.textContent = '\u2611';
        }
        else {
            col1.textContent = "Loading";
            icon.style = "font-size: 16px; float:right;";
            icon.textContent = '\u2610';
        }

        //set column contents
        col1.appendChild(icon);
        col2.textContent = object;
        if (is_printer) {
            col3.appendChild(a);
        }
        else {
            col3.textContent = temp.address;
        }
        col4.textContent = temp.port;
        col5.textContent = temp.series;
        col6.textContent = temp.version;

        //style columns
        col1.style.border = "1px solid #BBBBBB";
        col2.style.border = "1px solid #BBBBBB";
        col3.style.border = "1px solid #BBBBBB";
        col4.style.border = "1px solid #BBBBBB";
        col5.style.border = "1px solid #BBBBBB";
        col6.style.border = "1px solid #BBBBBB";

        //add entry to table
        row.appendChild(col1);
        row.appendChild(col2);
        row.appendChild(col3);
        if (is_printer) {
            row.appendChild(col4);
        }
        row.appendChild(col5);
        row.appendChild(col6);
        table.appendChild(row);
    }

    //sort table
    var rows, switching, i, x, y, shouldSwitch;
    switching = true;
    /* Make a loop that will continue until
    no switching has been done: */
    while (switching) {
        // Start by saying: no switching is done:
        switching = false;
        rows = table.rows;
        /* Loop through all table rows (except the
         first, which contains table headers): */
        for (i = 1; i < (rows.length - 1); i++) {
            // Start by saying there should be no switching:
            shouldSwitch = false;
            /* Get the two elements you want to compare,
            one from current row and one from the next: */
            x = rows[i].getElementsByTagName("TD")[1];
            y = rows[i + 1].getElementsByTagName("TD")[1];
            // Check if the two rows should switch place:
            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                // If so, mark as a switch and break the loop:
                shouldSwitch = true;
                break;
            }
        }
        if (shouldSwitch) {
            /* If a switch has been marked, make the switch
            and mark that a switch has been done: */
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }
    table.style.border = "1px solid #000";
}
populateTable(printer_table, printer_header, true, printers);
populateTable(device_table, device_header, false, devices);
