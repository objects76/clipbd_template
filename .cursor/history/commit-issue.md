# Git Push 실패 이슈 해결 과정

## 문제 상황

**발생 시간**: 2024년 7월 28일
**에러 메시지**:
```
remote: error: File preprocessing-ffmpeg-af.ipynb is 274.92 MB; this exceeds GitHub's file size limit of 100.00 MB
remote: error: GH001: Large files detected. You may want to try Git Large File Storage - https://git-lfs.github.com.
```

**원인**: Jupyter notebook 파일(`preprocessing-ffmpeg-af.ipynb`)의 출력 결과로 인해 파일 크기가 274.92MB로 GitHub의 100MB 제한을 초과

## 해결 과정

### 1단계: Jupyter Notebook 출력 클리어
```bash
jupyter nbconvert --clear-output --inplace preprocessing-ffmpeg-af.ipynb
```
- **결과**: 274.92MB → 7.4KB로 대폭 축소
- **문제**: Git 히스토리에 여전히 큰 파일이 남아있어 push 실패 지속

### 2단계: Git 히스토리에서 큰 파일 제거
```bash
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch preprocessing-ffmpeg-af.ipynb' --prune-empty --tag-name-filter cat -- --all
```
- **목적**: Git 히스토리에서 큰 파일을 완전히 제거
- **부작용**: 워킹 디렉토리에서도 파일이 삭제됨

### 3단계: 파일 복구 및 재커밋
```bash
# 이전 커밋에서 클리어된 파일 복구
git show 5712e79:preprocessing-ffmpeg-af.ipynb > preprocessing-ffmpeg-af.ipynb

# 파일 크기 확인 (7.4K)
ls -lh preprocessing-ffmpeg-af.ipynb

# 파일 추가 및 커밋
git add preprocessing-ffmpeg-af.ipynb
git commit -m "feat: add ffmpeg audio preprocessing notebook with cleared outputs"
```

### 4단계: Force Push
```bash
git fetch origin
git push --force
```
- **주의**: 히스토리가 변경되었으므로 `--force` 옵션 필요
- **결과**: 성공적으로 push 완료 (총 크기: 741.29 KiB)

## 교훈 및 예방책

### 1. .gitignore 설정
```gitignore
*.ipynb_checkpoints
# Large files - consider using Git LFS
```

### 2. Pre-commit Hook 설정 (선택사항)
```bash
# .git/hooks/pre-commit 파일 생성
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
jupyter nbconvert --clear-output --inplace *.ipynb 2>/dev/null || true
git add *.ipynb 2>/dev/null || true
EOF
chmod +x .git/hooks/pre-commit
```

### 3. 대용량 파일 관리
```bash
# Git LFS 설정
git lfs install
git lfs track "*.pth" "*.pkl" "*.h5" "*.model"
```

### 4. 정기적인 Notebook 출력 클리어
```bash
# 모든 notebook 출력 클리어
find . -name "*.ipynb" -exec jupyter nbconvert --clear-output --inplace {} \;
```

## 사용된 주요 명령어

| 명령어 | 목적 |
|--------|------|
| `jupyter nbconvert --clear-output --inplace` | Jupyter notebook 출력 제거 |
| `git filter-branch --index-filter` | Git 히스토리에서 파일 완전 제거 |
| `git show <commit>:<file>` | 특정 커밋에서 파일 복구 |
| `git push --force` | 히스토리 변경 후 강제 push |

## 결론

- ✅ 파일 크기: 274.92MB → 7.4KB 축소 성공
- ✅ Push 성공: 히스토리 정리 후 정상 업로드
- ⚠️ 주의사항: Force push로 인한 히스토리 변경
- 📝 향후 대책: Pre-commit hook 및 Git LFS 활용 고려