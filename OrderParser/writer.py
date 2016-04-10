__author__ = 'wonny'

import xlwt


def write_to_xls(order_list, output_path):
    workbook = xlwt.Workbook(encoding="utf-8")  # utf-8 인코딩 방식의 workbook 생성
    workbook.default_style.font.height = 20 * 11  # (11pt) 기본폰트설정 다양한건 찾아보길

    worksheet = workbook.add_sheet("Sheet1")  # 시트 생성
    font_style = xlwt.easyxf('font:name Arial, height 280; align: horz center')  # 폰트 스타일 생성

    print("새 파일 쓰는 중")

    worksheet.write(0, 0, "예약구분", font_style)
    worksheet.write(0, 1, "집하예정일", font_style)
    worksheet.write(0, 2, "수령인", font_style)
    worksheet.write(0, 3, "수령인 전화", font_style)
    worksheet.write(0, 4, "수령인 핸드폰", font_style)
    worksheet.write(0, 5, "우편번호", font_style)
    worksheet.write(0, 6, "배송지 주소", font_style)
    worksheet.write(0, 7, "운송장 번호", font_style)
    worksheet.write(0, 8, "주문번호", font_style)
    worksheet.write(0, 9, "상품명", font_style)
    worksheet.write(0, 10, "박스수량", font_style)
    worksheet.write(0, 11, "박스타입", font_style)
    worksheet.write(0, 12, "기본운임", font_style)
    worksheet.write(0, 13, "배송 유의사항", font_style)

    for row_val in range(len(order_list)):
        order = order_list[row_val]
        worksheet.write(row_val+1, 0, row_val, font_style)
        worksheet.write(row_val+1, 2, order['receiptor_name'], font_style)
        worksheet.write(row_val+1, 3, order['receiptor_phone'], font_style)
        worksheet.write(row_val+1, 5, order['zipcode'], font_style)
        worksheet.write(row_val+1, 6, order['address'], font_style)
        worksheet.write(row_val+1, 8, order['order_num'], font_style)
        worksheet.write(row_val+1, 9, order['product_name'] + "[" + order['product_option'] + "]", font_style)
        worksheet.write(row_val+1, 10, 1, font_style)
        worksheet.write(row_val+1, 13, order['caution'], font_style)

    # worksheet.col(0).width = 256* 10 #(key byte) 칸 너비 설정
    worksheet.col(1).width = 256 * 20  # 휴대폰 칸 너비 설정
    worksheet.col(3).width = 256 * 20  # 휴대폰 칸 너비 설정
    worksheet.col(4).width = 256 * 20  # 휴대폰 칸 너비 설정
    worksheet.col(6).width = 256 * 90  # 주소 칸 너비 설정
    worksheet.col(7).width = 256 * 20  # 운송잔 칸 너비 설정
    worksheet.col(8).width = 256 * 30  # 주문번호 칸 너비 설정
    worksheet.col(9).width = 256 * 120  # 상품명 칸 너비 설정
    worksheet.col(13).width = 256 * 60  # 배송메세지 칸 너비 설정

    print("새 파일 쓰기 완료, 저장 중")

    workbook.save(output_path)  # 엑셀 파일 저장 및 생성

    print("저장 완료")

