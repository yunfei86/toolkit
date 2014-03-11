<?php
set_include_path(get_include_path().PATH_SEPARATOR.dirname(__FILE__).get_include_path().PATH_SEPARATOR.dirname(__FILE__).'/results');
ini_set('display_errors', 'On');
error_reporting(E_ALL | E_STRICT);
date_default_timezone_set('America/Los_Angeles');
echo "<html>\n<head>\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\n<link rel=\"stylesheet\" type=\"text/css\" href=\"csss/framework.css\" />\n";
echo "</head>\n<body>\n";
echo "<table>\n<caption>Ion Unit Tests Run During the Month of <b>".strftime('%B')."</b></caption>\n";
echo "<tr><th id=\"topleft\">Test</th><th>Test Run Date</th><th>Success</th><th>Failures</th><th>Errors</th><th>Skips</th><th id=\"topright\">Total</th></tr>\n";
$htmlFile = '../results/'.strftime('%b%Y.html');
if(file_exists($htmlFile))
    include($htmlFile);
else echo '<tr>File ['.$htmlFile.'] Not Available</tr>';
echo "<tr><th id=\"bottomLeft\"></th><th id=\"blank\"></th><th id=\"blank\"></th><th id=\"blank\"></th><th id=\"blank\"></th><th id=\"blank\"></th><th id=\"bottomRight\"></th></tr>";
echo "</table>\n";
echo "<div id=\"info\">Page Maintained by: Ranjan.Muthumalai@Lifetech.com</div>";
echo "</body>\n</html>\n";
?>
