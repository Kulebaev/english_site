document.addEventListener('DOMContentLoaded', function () {
    function resizeMap() {
        var mapElement = document.getElementById('map');
        var windowWidth = window.innerWidth;

        if (windowWidth <= 350) {
            // Ширина экрана меньше или равна 545
            mapElement.className = 'smallMap_350';
        }else if (windowWidth <= 545) {
            // Ширина экрана меньше или равна 545
            mapElement.className = 'smallMap_540';
        } else if (mapElement.offsetWidth <= 767) {
            // Ширина карты меньше или равна 767
            mapElement.className = 'smallMap_600';
        } else {
            // Все остальные случаи
            mapElement.className = '';
        }

        // Обновление карты
        // Замените 'your-map-object' на объект карты, который у вас есть
        if (typeof yourMapObject !== 'undefined') {
            yourMapObject.container.fitToViewport();
        }
    }

    // Слушаем событие изменения размера окна
    window.addEventListener('resize', resizeMap);

    // Вызываем функцию при загрузке страницы
    window.addEventListener('load', resizeMap);
});
