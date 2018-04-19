FROM blang/latex:ubuntu

RUN mkdir /out
COPY ./build_resume.sh /bin/build_resume.sh
ENTRYPOINT [ "/bin/build_resume.sh" ]
