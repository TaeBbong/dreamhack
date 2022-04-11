<script src="filter.js"></script>
<pre id=param></pre>
<script>
    var param_elem = document.getElementById("param");
    var param = `<?php echo str_replace("`", "", $_GET["param"]); ?>`;
    if (typeof filter !== 'undefined') {
        for (var i = 0; i < filter.length; i++) {
            if (param.toLowerCase().includes(filter[i])) {
                param = "nope !!";
                break;
            }
        }
    }

    param_elem.innerHTML = param;
</script>
