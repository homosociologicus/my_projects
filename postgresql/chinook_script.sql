/*
-- albums' titles and artists' names
select "Title" as "AlbumTitle", "Name" as "ArtistName"
from "Album"
join "Artist" on "Album"."ArtistId"="Artist"."ArtistId"
order by "Title"
*/

-- full customers' names, sum and average of their invoices
select
	concat("FirstName", ' ', "LastName") as "CustomerName",
	sum("Total") as "TotalBill",
	round(avg("Total"), 2) as "AverageBill"
from "Customer"
join "Invoice" on "Customer"."CustomerId"="Invoice"."CustomerId"
group by "CustomerName"
order by "CustomerName"
