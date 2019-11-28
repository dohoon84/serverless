***<h>aergoLambdaCommandLine v0.1***<br>

```
setup
```
1.CLI 라이브러리를 내려받기 위한 가상의 공간을 마련합니다.
>python3 -m venv venv

2.활성화
>cd venv/bin <br>source activate

3.라이브러리 내려받기
>pip install -r requirements.txt

4.lamb 구동 확인
>python lamb.py

```
lamb-cli
```

1.블로코 구글계정으로 로그인 합니다. 타 구글계정으로의 로그인 접근은 불가합니다.
>$] python lamb.py login

2.CLI를 통해 gitlab repository를 생성합니다.
>$] python lamb.py create

3.접속을 종료합니다.
>$] python lamb.py logout
