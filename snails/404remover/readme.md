´localities.json´ was created using data obtained via:

    curl -o "admin_level_6.json" "http://overpass-api.de/api/interpreter?data=%5Bout:json%5D%5Btimeout:50%5D;area(3600062149)->.searchArea;relation%5Bboundary=administrative%5D%5Badmin_level=6%5D(area.searchArea);out%20body;"
    cat admin_level_6.json | jq '.elements[].id' | tr '\n' ','
