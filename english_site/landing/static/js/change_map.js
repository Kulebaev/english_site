document.addEventListener('DOMContentLoaded', function () {
    function resizeMap() {
        var mapElement = document.getElementById('map');
        var windowWidth = window.innerWidth;

        if (windowWidth <= 800) {
            mapElement.classList.add('smallMap');
        } else {
            mapElement.classList.remove('smallMap');
        }

        // Обновление карты
        // Замените 'your-map-object' на объект карты, который у вас есть
        if (typeof yourMapObject !== 'undefined') {
            yourMapObject.container.fitToViewport();
        }
    }

    // Слушаем событие изменения размера экрана
    window.addEventListener('resize', resizeMap);

    // Вызываем функцию при загрузке страницы
    window.addEventListener('load', resizeMap);
});