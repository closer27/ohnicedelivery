import xlwt


def write_to_xls(order_list):
    workbook = xlwt.Workbook(encoding="utf-8")  # utf-8 인코딩 방식의 workbook 생성
    workbook.default_style.font.height = 20 * 11  # (11pt) 기본폰트설정 다양한건 찾아보길
    xlwt.add_palette_colour("header_background_color", 0x21)
    workbook.set_colour_RGB(0x21, 207, 238, 209)
    xlwt.add_palette_colour("header_font_color", 0x22)
    workbook.set_colour_RGB(0x22, 43, 95, 24)

    worksheet = workbook.add_sheet("Sheet1")  # 시트 생성
    header_style = xlwt.easyxf('font:name Malgun Gothic, color header_font_color, height 220; '
                               'align: vert center; alignment: wrap True;'
                               'pattern:pattern solid, fore_colour header_background_color')  # 폰트 스타일 생성
    font_style = xlwt.easyxf('font:name Malgun Gothic, height 220; align: vert center; alignment: '
                             'wrap True;')  # 폰트 스타일 생성

    print("새 파일 쓰는 중")

    worksheet.row(0).height_mismatch = True
    worksheet.row(0).height = 54*20
    worksheet.write(0, 0, "수령인", header_style)
    worksheet.write(0, 1, "우편번호(생략가능)", header_style)
    worksheet.write(0, 2, "전체 주소", header_style)
    worksheet.write(0, 3, "연락처1\n(예) 0505-780-0505", header_style)
    worksheet.write(0, 4, "연락처2\n(예) 010-2879-6266", header_style)
    worksheet.write(0, 5, "상품명 (alt+enter 꼭 줄바꿈으로 구분할것, 독립된 셀에 적지마세요)\n(예) 김미진_무광하드_아이폰7_1개\n(예) "
                          "이진영_무광터프_아이폰7_3개", header_style)
    worksheet.write(0, 6, "배송메세지", header_style)

    for row_val in range(len(order_list)):
        order = order_list[row_val]
        worksheet.row(row_val+1).height_mismatch = True
        worksheet.row(row_val+1).height = 90*20
        worksheet.write(row_val+1, 0, order.recipient_name, font_style)
        worksheet.write(row_val+1, 2, order.address, font_style)
        worksheet.write(row_val+1, 3, order.recipient_phone, font_style)
        worksheet.write(row_val+1, 5, "[위탁][패키지][사은품1]" + order.recipient_name + "_" + order.product_option + "_1개", font_style)
        worksheet.write(row_val+1, 6, order.caution, font_style)
        worksheet.write(row_val+1, 7, order.product_name, font_style)

    # worksheet.col(0).width = 256* 10 #(key byte) 칸 너비 설정
    worksheet.col(0).width = 256 * 7  # 휴대폰 칸 너비 설정
    worksheet.col(1).width = 256 * 18  # 휴대폰 칸 너비 설정
    worksheet.col(2).width = 256 * 69  # 휴대폰 칸 너비 설정
    worksheet.col(3).width = 256 * 18  # 주소 칸 너비 설정
    worksheet.col(4).width = 256 * 18  # 운송잔 칸 너비 설정
    worksheet.col(5).width = 256 * 61  # 주문번호 칸 너비 설정
    worksheet.col(6).width = 256 * 11  # 상품명 칸 너비 설정
    worksheet.col(7).width = 256 * 61  # 참고용 칸

    print("새 파일 쓰기 완료, 저장 중")

    from io import BytesIO
    f = BytesIO()
    workbook.save(f)  # 엑셀 파일 저장 및 생성
    f.seek(0)
    print("저장 완료")

    return f
