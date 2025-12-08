# FDS-Dev (Flamehaven Doc Sanity for Developers)

<div align="center">

<p align="center">
  <img src="docs/Doc Sanity Logo.png" alt="FDS-Dev Logo" width="420">
</p>

**[English](README.md) | [한국어](README_KR.md)**

[![PyPI version](https://badge.fury.io/py/fds-dev.svg)](https://badge.fury.io/py/fds-dev)
[![Python Versions](https://img.shields.io/pypi/pyversions/fds-dev.svg)](https://pypi.org/project/fds-dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI/CD Pipeline](https://github.com/flamehaven01/FDS-Dev/actions/workflows/ci.yml/badge.svg)](https://github.com/flamehaven01/FDS-Dev/actions/workflows/ci.yml)
[![Test Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen.svg)](https://github.com/flamehaven01/FDS-Dev)
[![Code Quality](https://img.shields.io/badge/quality-A+-blue.svg)](https://github.com/flamehaven01/FDS-Dev)
[![SIDRCE Certified](https://img.shields.io/badge/SIDRCE-0.896%20Certified-green.svg)](https://github.com/flamehaven01/FDS-Dev)

**초고속 구조 인식 문서 린터, AI 기반 번역 기능 탑재**

글로벌 개발자 커뮤니티를 위해 제작되었습니다. 모국어로 문서와 코드 주석을 작성하면, FDS-Dev가 즉시 프로덕션 수준의 영어로 번역합니다.

[핵심 기능](#핵심-기능) • [빠른 시작](#빠른-시작) • [문서](docs/) • [기여하기](#기여하기) • [지원](#지원)

</div>

---

## 문제점

한국, 일본, 중국, 독일 또는 전 세계 어디에서나 온 재능 있는 개발자라면, 코드는 훌륭하지만 영어로 문서와 주석을 작성하는 것이 부담스러울 것입니다. 이는 작업 속도를 늦추고 글로벌 오픈소스 커뮤니티와 공유하는 데 장벽이 됩니다.

`markdownlint`나 `Vale` 같은 기존 린터는 훌륭하지만, 영어 중심적이라 이 핵심 문제를 해결하지 못합니다.

## 해결책: FDS-Dev

FDS-Dev는 두 가지 도구를 하나로 결합했습니다:

1.  **초고속 린터:** 문서의 깔끔하고 전문적인 구조를 보장합니다.
2.  **AI 기반 번역기:** 모국어로 작성된 문서와 주석을 자연스럽고 유창한 영어로 자동 번역합니다.

**영어 걱정은 그만하고, 코드에만 집중하세요.**

## FDS-Dev를 선택해야 하는 이유

### 코드 레벨 국제화라는 새로운 카테고리

기존 린터(markdownlint, Vale)는 영어 문서를 기준으로 형식을 검사할 뿐이고, 일반 번역기는 코드 블록을 깨거나 기술 용어를 훼손합니다. FDS-Dev는 문서, 코드 주석, 독스트링을 구조적으로 이해해 비영어권 개발자가 별도의 영어 작성 없이 글로벌 OSS에 참여하도록 돕습니다.

### 실제로 해결하는 문제

- **언어 장벽 해소**: README, 아키텍처 문서, 인라인 주석, 독스트링을 영어로 변환하면서 코드 구조는 그대로 유지합니다.
- **문서 품질 보증**: 필수 섹션 존재 여부나 헤더 순서 같은 구조 규칙을 강제해 항상 일정한 품질을 유지합니다.

### FDS-Dev만의 차별점

1. **AI 기반 코드 인지 번역**
   - `CodeCommentParser`로 Markdown, Python 독스트링, 인라인 주석을 파싱해 번역 대상과 코드 블록을 구분합니다.
   - `TechnicalTermDatabase`가 CamelCase, snake_case 등 식별자를 보존해 API 명칭이 흐트러지지 않습니다.
   - `TranslationQualityOracle`가 번역 결과를 Omega(Ω) 점수로 평가해 기준 미달 번역은 재시도하거나 거부할 수 있습니다.

2. **초고속 구조 인식 린터**
   - `.fds_cache.json` 캐시와 병렬 실행으로 대규모 문서를 빠르게 검증합니다.
   - “License 섹션 필수”, “Installation이 Usage보다 먼저” 같은 구조 규칙까지 검사합니다.

3. **유연한 번역 프로바이더**
   - 기본 py-googletrans는 설정 없이 바로 사용 가능.
   - `.fdsrc.yaml`에서 DeepL, MyMemory, LibreTranslate 등으로 쉽게 전환해 품질/예산에 맞춘 환경을 구축할 수 있습니다.

4. **커뮤니티 파급력**
   - 비영어권 개발자가 더 쉽게 PR을 제출하고 국제 협업을 진행할 수 있어 오픈소스 생태계를 확장시킵니다.
   - 적극적으로 개발이 진행 중이므로 Star, Issue, PR이 곧바로 로드맵에 반영됩니다.

## 핵심 기능

- **구조 인식 린팅:** 단순한 스타일 검사를 넘어섭니다. 섹션 순서 강제, 특정 헤더 요구, 문서 전체 구조 검증.
- **링크 무결성 검사:** `broken-link-check` 규칙을 켜면 누락된 앵커, 존재하지 않는 파일, 접근 불가한 URL을 사전에 감지할 수 있습니다.
- **자동 번역:** 한국어, 중국어, 일본어 등의 Markdown 파일과 소스 코드 주석을 영어로 번역합니다.
- **간편한 설정:** 단일 `.fdsrc.yaml` 파일로 모든 것을 제어합니다.
- **속도 최적화:** 최대 성능을 위해 설계된 핵심 컴포넌트.

## 빠른 시작

```bash
# 설치
pip install --upgrade fds-dev

# 설정 초기화
fds init

# 첫 린트 실행
fds lint README.md
```

### [>] 10분 빠른 시작 가이드

**1. 문서 린트 검사** - 구조적 문제 확인
```bash
fds lint README.ko.md
```

**2. 영어로 번역** - 글로벌 수준의 문서를 즉시 생성
```bash
# README.ko.md -> README.md 번역
fds translate README.ko.md --output README.md

# 소스 코드 주석을 제자리에서 번역
fds translate my_app/main.py --in-place
```

**3. 실행 가능한 예제 확인**
```bash
# 리포지토리를 클론하고 예제 실행
git clone https://github.com/flamehaven01/FDS-Dev.git
cd FDS-Dev
pip install -e .
python examples/basic_usage.py
```

[+] **다음 단계**: 프로덕션 패턴은 [`examples/`](examples/)를, 팀 배포는 [`docs/ENTERPRISE.md`](docs/ENTERPRISE.md)를 참조하세요.

```bash
# 소스 코드 파일의 주석을 제자리에서 번역
fds translate my_app/main.py --in-place
```

### 설정 및 캐시 처리
- `fds lint`/`fds translate`에 넘긴 경로를 시작점으로 `.fdsrc.yaml`을 탐색합니다. 각 문서 트리마다 별도 규칙을 둘 수 있으며, 작업 디렉터리를 옮길 필요가 없습니다.
- 린트 캐시(`.fds_cache.json`)는 대상 경로나 파일과 같은 위치에 저장되어 트리별로 스코프가 분리됩니다.
- `translate`는 자동 언어 감지 시 신뢰도( confidence )를 출력하고, 소스/타깃 언어가 같으면 안전하게 건너뜁니다.

## CLI 명령어

- `fds lint <path>`: `.fdsrc.yaml`에 정의된 구조 린팅 규칙(옵션으로 `broken-link-check` 포함)을 실행합니다.
- `fds translate <path> [--output OUTPUT | --in-place]`: Markdown/소스 파일을 영어로 번역하면서 코드 블록과 식별자를 유지합니다.
- `fds lint --help` / `fds translate --help`: 사용 가능한 모든 옵션을 확인할 수 있습니다.

링크 검사는 `.fdsrc.yaml` 설정만으로 제어되며, 규칙을 켜면 `fds lint` 결과에 깨진 링크도 일반 린트 오류처럼 보고됩니다.

## 번역 제공자

FDS-Dev는 여러 번역 제공자를 지원합니다. `.fdsrc.yaml` 파일에서 선호하는 제공자를 설정할 수 있습니다.

| 제공자                  | 기본값?        | API 키 | 비용                  | 품질    | 안정성      | 권장 사용 사례                     |
| :------------------------ | :-------------- | :------ | :-------------------- | :--------- | :------------- | :--------------------------------------- |
| **Google Translate (Free)** | **✅ (기본값)**  | 없음    | 무료                  | 높음       | **불안정**¹  | 개인 프로젝트, 빠른 테스트, 일반 문서 |
| **DeepL**                 | ❌              | **필수** | 제한된 무료 티어/유료  | **매우 높음** | 매우 높음      | 프로덕션, 상업용, 공식 문서      |
| **MyMemory**                | ❌              | 없음    | 무료                  | 보통     | 보통         | 간단한 스크립트, 임시 사용            |
| **LibreTranslate**          | ❌              | 없음    | 무료 (자체 호스팅)    | 보통²    | **사용자 관리** | 사설 서버, 오프라인, 완전한 제어       |

> ¹ 비공식 API를 사용하므로 예고 없이 작동이 중단될 수 있습니다.
> ² 품질은 사용자가 직접 호스팅하는 모델에 따라 달라집니다.

기본값이 아닌 제공자를 사용하려면 `.fdsrc.yaml` 파일에서 설정하세요. API 키가 필요한 제공자의 경우 환경 변수 사용을 강력히 권장합니다.

**DeepL 예제:**
```yaml
# .fdsrc.yaml
translator:
  provider: 'deepl'
  providers:
    deepl:
      # FDS_DEEPL_API_KEY 환경 변수 사용을 권장합니다.
      api_key: null
      timeout: 5   # 초 단위 기본 타임아웃 (서비스 지연 시 CLI 멈춤 방지)
```

## 배포 및 자동화

### 지속적 통합 (CI)

GitHub Actions는 `main` 브랜치를 대상으로 하는 모든 푸시 및 풀 리퀘스트에 대해 Python 3.9–3.11에서 테스트 스위트를 자동으로 실행하고 릴리스 아티팩트를 빌드합니다. 워크플로우 정의는 `.github/workflows/ci.yml`에서 확인할 수 있습니다.

### PyPI 자동 릴리스

`v*` 패턴으로 커밋에 태그를 지정하면(예: `v0.2.0`) `.github/workflows/release.yml`이 트리거되어 `python -m build`로 프로젝트를 빌드하고 `PYPI_API_TOKEN` 시크릿을 사용하여 PyPI에 게시합니다.

### 공식 Docker 이미지

제공된 `Dockerfile`을 사용하여 CLI를 컨테이너 이미지로 배포할 수 있습니다:

```bash
docker build -t fds-dev .
docker run --rm fds-dev lint README.md
```

이미지는 패키지를 전역으로 설치하고 `fds` 진입점을 노출하므로 모든 CLI 명령을 직접 실행할 수 있습니다.

## 기여하기

FDS-Dev는 초기 개발 단계입니다. 기여를 환영합니다!

전체 기여 체크리스트와 릴리스 워크플로는 [CONTRIBUTING.md](CONTRIBUTING.md)에서 확인하세요.

커뮤니티의 기여를 환영합니다! 다음과 같은 방법으로 도움을 주실 수 있습니다:

### 기여 방법

1. **이슈 제보**: 버그를 발견하셨나요? [이슈 등록](https://github.com/flamehaven01/FDS-Dev/issues)
2. **기능 제안**: 아이디어가 있으신가요? [토론](https://github.com/flamehaven01/FDS-Dev/discussions)에서 공유하세요
3. **풀 리퀘스트 제출**: 버그 수정 또는 기능 추가
4. **문서 개선**: 문서를 더욱 좋게 만들어주세요

### 개발 환경 설정

```bash
# 저장소 클론
git clone https://github.com/flamehaven01/FDS-Dev.git
cd FDS-Dev

# 개발 모드로 설치
pip install -e .

# 테스트 실행
pytest tests/ -v

# 린터 실행
flake8 fds_dev/
```

### 코드 품질 기준

- 테스트 커버리지 ≥ 90%
- 모든 테스트 통과 (100/105 예상)
- PEP 8 스타일 가이드 준수
- 공개 API에 docstring 추가
- 새 기능에 대한 문서 업데이트

---

## 팀 및 엔터프라이즈

FDS-Dev는 개인 개발자부터 엔터프라이즈 배포까지 확장 가능합니다:

- [#] **자체 호스팅** - 완전한 데이터 제어, 에어갭 환경 지원
- [#] **CI/CD 통합** - GitHub Actions, GitLab CI, Jenkins 즉시 사용 가능
- [&] **커스텀 배포** - Docker, Kubernetes, 모노레포 지원
- [W] **SLA 및 지원** - 엔터프라이즈 계약 가능

[>] **자세히 보기**: 배포 아키텍처, 보안 제어, 팀 워크플로우는 [`docs/ENTERPRISE.md`](docs/ENTERPRISE.md)를 참조하세요.

---

## 지원

### 문서

- **[번역 알고리즘](docs/TRANSLATION_ALGORITHM.md)** - 완전한 파이프라인 설명
- **[아키텍처 가이드](docs/ARCHITECTURE.md)** - 시스템 설계 문서
- **[문제 해결](docs/TROUBLESHOOTING.md)** - 일반적인 문제와 해결책

### 도움 받기

- **GitHub Issues**: [버그 제보 또는 기능 요청](https://github.com/flamehaven01/FDS-Dev/issues)
- **GitHub Discussions**: [질문 및 아이디어 공유](https://github.com/flamehaven01/FDS-Dev/discussions)
- **Email**: [info@flamehaven.space](mailto:info@flamehaven.space)

### 커뮤니티

- **웹사이트**: [flamehaven.space](https://flamehaven.space)
- **저장소**: [github.com/flamehaven01/FDS-Dev](https://github.com/flamehaven01/FDS-Dev)

---

## 라이센스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

---

## 감사의 말

FDS-Dev는 다음 기술로 구축되었습니다:
- **py-googletrans** - 무료 Google Translate API
- **DeepL API** - 고품질 번역 백엔드
- **click** - 아름다운 CLI 프레임워크
- **pytest** - 테스팅 프레임워크

모든 기여자와 오픈소스 커뮤니티에 특별한 감사를 드립니다!

---

<div align="center">

**Flamehaven이 ❤️를 담아 제작했습니다 - [Flamehaven](https://flamehaven.space)**

[⬆ 맨 위로](#fds-dev-flamehaven-doc-sanity-for-developers)

</div>

