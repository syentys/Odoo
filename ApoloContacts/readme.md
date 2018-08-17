# Contacts Module #

This module customize the module contacts according to Apol Specification.



### Author


<a href="https://www.syentys.com">SYENTYS</a>



### Modifications

* **Add subfolders**

<ul> 
	<ol>
            <li> Customers 							</li>
			<li> Prospects 							</li>
			<li> Suppliers 							</li>
			<li> Distributors 						</li>
			<li> All								</li>
			<li> Contact Tags						</li>
	</ol>
</ul>


```
mermaid

graph LR;

    ALL-->CUSTOMERS;
    ALL-->PROSPECTS;
    ALL-->SUPPLIERS;
    ALL-->DISTRIBUTORS;
    CUSTOMERS-->PERSON ;
    PROSPECTS-->CUSTOMERS;
    DISTRIBUTORS-->COMPANY;
    SUPPLIERS-->PERSON;
    SUPPLIERS-->COMPANY;
```

* **Customization of the contacts form**
* **Opening Hours in notebook**
* **Contacts Geolocalisation in notebook**


#### To improve
---------------

```
markdown
* Geolocalisation
* Inactive Partners (timedelta)
* ir_attachment (numbers)
```
