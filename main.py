import subprocess
import re
from rkr_gst.RKRGST import RKRGST

def source_code_to_token(source_code_path, output_filename = None):
    result = subprocess.run(['java', '-cp', '../../tcc/antlr:../../tcc/antlr/antlr-4.9.2-complete.jar', 'org.antlr.v4.gui.TestRig', 'C', 'translationUnit', '-tokens', source_code_path], stdout=subprocess.PIPE)
    raw_tokenized = result.stdout.decode('utf-8')
    code = ''
    for token in raw_tokenized.split('\n'):
        match, *_ = re.findall(r'(?<=\,\<).+?(?=\>\,)', token)
        if match[0] == '\'':
            match = match[1:-1]
        if match == 'EOF':
            break
        is_char = re.match(r'\[a-Z\]', match)
        if not is_char and match in [';', '{', '}']:
            code += match + '\n'
            continue
        code += match + ' ' if not is_char else match + '\n'
    code = re.sub(r'[\{\}\;\n]', '', code)
    if output_filename:
        with open(output_filename, 'w') as token_file:
            token_file.write(code)
    return code

if __name__ == '__main__':
    code1 = source_code_to_token('../../tcc/antlr/example.c', './out1')
    code2 = source_code_to_token('../../tcc/antlr/example2.c', './out2')
    matches = RKRGST.run(code1, code2, 3, 9)
    sim = 0
    code_len = len(code1)
    for match in matches:
        sim += 100 * match.length / code_len
    print('Similaridade: {}'.format(sim))