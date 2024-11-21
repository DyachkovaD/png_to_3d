import segno


def make_qr(url: str, scale=5, border=1) -> None:
    """
    Делает QR-код в формате png из строки
    url - строка для кодирования
    scale - размер QR изображения ( коэффициент масштабирования )
    border - границы QR кода
    """

    qr = segno.make_qr(url)
    qr.save(
        'input.png',
        scale=scale,
        border=border,
    )

    print('QR-код создан')

make_qr('https://www.softack.ru')
