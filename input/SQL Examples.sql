-- Query 1

WITH gastos_por_cliente AS (
 SELECT
   c.customerid,
   c.firstname  || ' ' || c.lastname  AS NomeCompleto,
   c.Country,
   SUM(i.Total) AS TotalGastos
 FROM Customer c
 JOIN Invoice i ON c.customerid = i.customerid
 GROUP BY c.customerid, c.firstname , c.lastname , c.Country
)
SELECT
 NomeCompleto,
 Country,
 TotalGastos,
 RANK() OVER (ORDER BY TotalGastos DESC) AS Posicao
FROM gastos_por_cliente
ORDER BY TotalGastos DESC
LIMIT 10;

-- Query 2

WITH vendasmensais AS (
 SELECT
   DATE_FORMAT(i.InvoiceDate, '%Y-%m') AS MesAno,
   SUM(i.Total) AS TotalMensal
 FROM Invoice i
 WHERE year(i.invoicedate) = 2021
 GROUP BY DATE_FORMAT(i.InvoiceDate, '%Y-%m')
)
SELECT
 MesAno,
 TotalMensal,
 SUM(TotalMensal) OVER (ORDER BY MesAno) AS TotalAcumulado
FROM vendasmensais
ORDER BY MesAno;

-- Query 3

SELECT
 i.invoiceid ,
 i.invoicedate,
 i.Total AS ValorAtual,
 i.Total - LAG(i.Total) OVER (PARTITION BY i.customerid  ORDER BY i.invoicedate) AS DiferencaParaAnterior
FROM Invoice i
WHERE i.customerid  = 42
ORDER BY i.invoicedate;    

-- Query 4

WITH vendasporfaixa AS (
 SELECT
   t.trackid ,
   t.Name AS NomeFaixa,
   g.Name AS NomeGenero,
   COUNT(il.invoicelineid) AS TotalVendas
 FROM Track t
 JOIN Genre g ON t.genreid  = g.genreid
 JOIN invoiceline il ON t.trackid  = il.trackid
 GROUP BY t.trackid , t.Name, g.Name
),
rankfaixas AS (
 SELECT
   NomeFaixa,
   NomeGenero,
   TotalVendas,
   ROW_NUMBER() OVER (PARTITION BY NomeGenero ORDER BY TotalVendas DESC) AS PosicaoGenero
 FROM vendasporfaixa
)
SELECT
 NomeGenero,
 NomeFaixa,
 TotalVendas
FROM rankfaixas
WHERE PosicaoGenero <= 3
ORDER BY NomeGenero, TotalVendas DESC;

-- Question 5

WITH vendasordenadas AS (
 SELECT
   t.trackid ,
   t.Name AS NomeFaixa,
   il.Quantity,
   i.invoicedate ,
   ROW_NUMBER() OVER (PARTITION BY t.trackid  ORDER BY i.invoicedate) AS OrdemPorFaixa
 FROM Track t
 JOIN invoiceline il ON t.trackid  = il.trackid
 JOIN Invoice i ON il.invoiceid = i.invoiceid
)
SELECT
 vo.trackid,
 vo.NomeFaixa,
 vo.Quantity AS QuantidadeAtual,
 LEAD(vo.Quantity) OVER (PARTITION BY vo.trackid ORDER BY vo.invoicedate) AS QuantidadeProxima,
 (vo.Quantity - LEAD(vo.Quantity) OVER (PARTITION BY vo.trackid ORDER BY vo.invoicedate)) AS Variacao
FROM vendasordenadas vo
WHERE OrdemPorFaixa = 1
ORDER BY vo.trackid;

-- Query 6

WITH faturascliente AS (
 SELECT
   i.customerid ,
   i.invoicedate ,
   LAG(i.invoicedate) OVER (PARTITION BY i.customerid ORDER BY i.invoicedate) AS DataAnterior
 FROM Invoice i
),
diferencas AS (
 SELECT
   fc.customerid,
   TIMESTAMPDIFF(SECOND, fc.DataAnterior, fc.invoicedate) AS DiasEntreFaturas
 FROM faturascliente fc
 WHERE fc.DataAnterior IS NOT NULL
),
mediaporcliente AS (
 SELECT
   d.customerid,
   AVG(d.DiasEntreFaturas) AS MediaDias
 FROM diferencas d
 GROUP BY d.customerid
)
SELECT
 c.customerid,
 c.firstname  || ' ' || c.lastname  AS NomeCompleto,
 ROUND(mp.MediaDias, 2) AS MediaDiasEntreFaturas
FROM mediaporcliente mp
JOIN Customer c ON mp.customerid = c.customerid
ORDER BY MediaDiasEntreFaturas;

-- Query 7

WITH datascompras AS (
 SELECT
   i.customerid ,
   MIN(i.invoicedate) AS DataPrimeira,
   MAX(i.invoicedate) AS DataUltima,
   COUNT(i.invoiceid) AS TotalFaturas
 FROM Invoice i
 GROUP BY i.customerid
 HAVING COUNT(i.invoiceid) > 1
)
SELECT
 c.customerid,
 c.firstname  || ' ' || c.lastname  AS NomeCompleto,
 dc.DataPrimeira,
 dc.DataUltima,
 EXTRACT(DAY FROM (dc.DataUltima - dc.DataPrimeira)) AS DiasEntreCompras
FROM datascompras dc
JOIN Customer c ON dc.customerid = c.customerid
ORDER BY DiasEntreCompras DESC;

-- Query 8

WITH receitaporfuncionario AS (
 SELECT
   e.employeeid ,
   e.firstname  || ' ' || e.lastname  AS NomeCompleto,
   e.Title,
   SUM(i.Total) AS ReceitaTotal
 FROM Employee e
 JOIN Customer c ON e.employeeid  = c.supportrepid
 JOIN Invoice i ON c.customerid  = i.customerid
 GROUP BY e.employeeid , e.firstname , e.lastname , e.Title
)
SELECT
 employeeid,
 NomeCompleto,
 Title,
 ReceitaTotal,
 DENSE_RANK() OVER (ORDER BY ReceitaTotal DESC) AS Posicao
FROM receitaporfuncionario
ORDER BY ReceitaTotal DESC;

-- Query 9

WITH vendassemanais AS (
 SELECT
   WEEK(i.invoicedate) AS InicioSemana,
   SUM(i.Total) AS ReceitaSemanal
 FROM Invoice i
 WHERE YEAR(i.invoicedate) = 2021
 GROUP BY WEEK(i.invoicedate)
)
SELECT
 vs.InicioSemana,
 vs.ReceitaSemanal,
 ROUND(
   AVG(vs.ReceitaSemanal)
   OVER (
     ORDER BY vs.InicioSemana
     ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
   ), 2
 ) AS MediaMovel4Semanas
FROM vendassemanais vs
ORDER BY vs.InicioSemana;

-- Query 10

WITH contagemfaixas AS (
 SELECT
   pt.playlistid,
   COUNT(pt.trackid) AS TotalFaixas
 FROM playlisttrack pt
 GROUP BY pt.playlistid
 HAVING COUNT(pt.trackid) > 50
),
generoporplaylist AS (
 SELECT
   pt.playlistid,
   t.genreid ,
   g.Name AS NomeGenero,
   COUNT(*) AS QtdePorGenero,
   ROW_NUMBER() OVER (
     PARTITION BY pt.playlistid
     ORDER BY COUNT(*) DESC
   ) AS PosicaoGenero
 FROM playlisttrack pt
 JOIN Track t ON pt.trackid  = t.trackid
 JOIN Genre g ON t.genreid  = g.genreid
 GROUP BY pt.playlistid , t.genreid, g.Name
)
SELECT
 p.playlistid,
 p.Name AS NomePlaylist,
 gp.NomeGenero AS GeneroPredominante
FROM Playlist p
JOIN contagemfaixas cf ON p.playlistid  = cf.playlistid
JOIN generoporplaylist gp
 ON p.playlistid = gp.playlistid
 AND gp.PosicaoGenero = 1
ORDER BY p.playlistid;




SELECT RankedGenres.PlaylistId AS PlaylistId, p.Name AS PlaylistName, g.Name AS PredominantGenre FROM 
  (SELECT pt.PlaylistId, t.GenreId, COUNT(*) AS TrackCount, 
       RANK() OVER (PARTITION BY pt.PlaylistId ORDER BY COUNT(*) DESC) AS GenreRank 
          FROM chinook.playlisttrack pt 
              JOIN chinook.track t ON pt.TrackId = t.TrackId 
		   GROUP BY pt.PlaylistId, t.GenreId 
           HAVING COUNT(*) > 50) AS RankedGenres 
             JOIN chinook.genre g ON RankedGenres.GenreId = g.GenreId 
             WHERE RankedGenres.GenreRank = 1;

