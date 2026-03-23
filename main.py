
CSV_FILE = '../Mars_Base_Inventory_List.csv'
DANGER_FILE = 'Mars_Base_Inventory_danger.csv'
FLAMMABILITY_THRESHOLD = 0.7

HEADER = ['Substance', 'Weight (g/cm³)', 'Specific Gravity', 'Strength', 'Flammability']

IDX_SUBSTANCE = 0
IDX_WEIGHT = 1
IDX_SPECIFIC_GRAVITY = 2
IDX_STRENGTH = 3
IDX_FLAMMABILITY = 4


def read_csv(filename):
  
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        data = []
        for line in lines:
            line = line.strip()
            if line:
                row = line.split(',')
                data.append(row)
        return data

    except FileNotFoundError:
        print(f'오류: {filename} 파일을 찾을 수 없습니다.')
        return []
    except IOError as e:
        print(f'파일 읽기 오류: {e}')
        return []


def print_inventory(data):
    """CSV 데이터를 헤더 포함 전체 출력한다."""
    if not data:
        print('출력할 데이터가 없습니다.')
        return

    for row in data:
        print(', '.join(row))


def convert_to_list(data):
    """
    CSV 2차원 리스트를 딕셔너리 리스트로 변환한다.
    헤더 행은 제외하고 데이터 행만 변환한다.
    """
    if len(data) < 2:
        print('변환할 데이터가 충분하지 않습니다.')
        return []

    inventory = []
    for row in data[1:]:
        if len(row) != len(HEADER):
            continue
        item = {
            'substance': row[IDX_SUBSTANCE].strip(),
            'weight': row[IDX_WEIGHT].strip(),
            'specific_gravity': row[IDX_SPECIFIC_GRAVITY].strip(),
            'strength': row[IDX_STRENGTH].strip(),
            'flammability': row[IDX_FLAMMABILITY].strip(),
        }
        inventory.append(item)
    return inventory


def get_flammability_value(item):
    
    try:
        return float(item['flammability'])
    except ValueError:
        return 0.0


def sort_by_flammability(inventory):
    
    return sorted(inventory, key=get_flammability_value, reverse=True)


def filter_dangerous(inventory, threshold=FLAMMABILITY_THRESHOLD):
   
    result = []
    for item in inventory:
        if get_flammability_value(item) >= threshold:
            result.append(item)
    return result


def print_dangerous(dangerous_items):
    
    if not dangerous_items:
        print('인화성 위험 물질이 없습니다.')
        return

    print(f'{"Substance":<25} {"Flammability":>12}')
    print('-' * 40)
    for item in dangerous_items:
        print(f"{item['substance']:<25} {item['flammability']:>12}")
    print(f'\n총 {len(dangerous_items)}개의 위험 물질 발견.')


def save_to_csv(inventory, filename):
   
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(','.join(HEADER) + '\n')
            for item in inventory:
                row = [
                    item['substance'],
                    item['weight'],
                    item['specific_gravity'],
                    item['strength'],
                    item['flammability'],
                ]
                f.write(','.join(row) + '\n')
        print(f'저장 완료: {filename}')

    except IOError as e:
        print(f'파일 저장 오류: {e}')


def main():
    separator = '=' * 60

    print(separator)
    print('  화성 기지 인화성 물질 분류 및 격리 시스템')
    print(separator)
    
    print('\n[과제 1] Mars_Base_Inventory_List.csv 읽기 및 출력')
    print('-' * 60)
    raw_data = read_csv(CSV_FILE)
    print_inventory(raw_data)


    print('\n[과제 2] Python 리스트 객체로 변환')
    print('-' * 60)
    inventory = convert_to_list(raw_data)
    print(f'총 {len(inventory)}개 물질을 리스트로 변환 완료.')


    print('\n[과제 3] 인화성 높은 순으로 정렬')
    print('-' * 60)
    sorted_inventory = sort_by_flammability(inventory)
    print(f'{"Substance":<25} {"Flammability":>12}')
    print('-' * 40)
    for item in sorted_inventory:
        print(f"{item['substance']:<25} {item['flammability']:>12}")


    print(f'\n[과제 4] 인화성 지수 {FLAMMABILITY_THRESHOLD} 이상 위험 물질 목록')
    print('-' * 60)
    dangerous_items = filter_dangerous(sorted_inventory)
    print_dangerous(dangerous_items)


    print('\n[과제 5] 위험 물질 목록을 CSV 파일로 저장')
    print('-' * 60)
    save_to_csv(dangerous_items, DANGER_FILE)


if __name__ == '__main__':
    main()
