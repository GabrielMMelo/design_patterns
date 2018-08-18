# DESIGN PATTERNS

Official Emakers Júnior LaTeX docs templates. 💜

## Technologies used 

- [MikTeX 2.9](https://miktex.org/download)
- `abntex2` TeX package;
- `titlesec` TeX package;
- [nlatexdb](https://ctan.org/pkg/nlatexdb) package;
- `MySQL`;
- [Mono](https://www.mono-project.com/) .NET framework;


## Folders
- `layouts/`

    Aux files to include. Here, files has `\dev`, `\newcommand` and all reusable stuff.

- `out/`

    Generated *.pdf* files.  We have been used `pdflatex` compiler.

- `img/`
    
    All image files.

- `docs/`
    
    Support files. Tutorials, guides and documentation.

## Documents

- `doc.tex`
    
    General purpose document. 

- `contract.tex`
    
    Official services contract.

- `volunteer.tex`
    
    Volunteer term.

- `agenda.tex`

    A list of items to be discussed at a meeting.

- `minutes.tex`
     
    A summary or record of what is said or decided at a formal meeting.

- `announcement.tex`

	A doc to jobs e elections announcements.


## Install/Usage `nlatexbd`

### Installing on Windows

1. Download `nlatexdb` to the project root;

2. Install `Mono` for Windows;

3. Download `Mysql.Data.dll`;

4. Install .dll on GAC;

```
gacutil -i MySql.Data.dll 
```

5. In `Mono` installing folder (C:\Program Files\Mono\etc\mono\4.5), add the code below in `machine.config` file:

```
 <add name="MySQL Data Provider" invariant="MySql.Data.MySqlClient" description=".Net Framework Data Provider for MySQL" 
      type="MySql.Data.MySqlClient.MySqlClientFactory, MySql.Data, Version=8.0.10.0, Culture=neutral, PublicKeyToken=c5687fc88969c44d" />
```

Where `Version=` is the same version number that's there when you installed the dll in GAC.



### Using on Windows

Execute the code below:

```
mono --runtime=v4.0 nlatexdb.exe -e utf-8 -p FILE_NAME.tex
```

> **-p** is used to call `pdflatex` on result.

> **-e** is used to set encoding to input/output.

### References

- For mono/MySQL #1 -> https://sourceforge.net/p/nlatexdb/wiki/MySQL%20and%20Mono/

- For mono/MySQL #2 -> https://stackoverflow.com/questions/3987266/mysql-connector-with-mod-mono-and-mono-2-6-7

- For `nlatexdb` examples -> https://ctan.org/tex-archive/support/nlatexdb/examples

- For MySQL connection strings -> https://www.connectionstrings.com/mysql-connector-net-mysqlconnection/



