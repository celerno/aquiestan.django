var geoToPixel = function (lat, lon) {
    const lat_start= 32.509600774356244;
    const lon_start= -115.05720122875945;
    const lat_end= 26.410299210278374;
    const lon_end= -108.24102851631902;

    return {
        lat: (lat/(lat_start-lat_end))*100,
        lon: (lon/(lon_start-lon_end))*100
    }
}