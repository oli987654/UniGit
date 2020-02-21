%% If you want to change this file you probably should look at classes.dtx
%% Changes: 12/05: added quote-environment

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{exercise}
              [2014/13/09 v0.02]
%% Defaults options: 11pt, a4paper, twoside, final
\newcommand\@ptsize{}
\newif\if@restonecol
\newif\if@titlepage %% note: titlepages are NOT supported
\@titlepagefalse
%% Set paper sizes
\DeclareOption{a4paper}
   {\setlength\paperheight {297mm}%
    \setlength\paperwidth  {210mm}}
\DeclareOption{a5paper}
   {\setlength\paperheight {210mm}%
    \setlength\paperwidth  {148mm}}
\DeclareOption{b5paper}
   {\setlength\paperheight {250mm}%
    \setlength\paperwidth  {176mm}}
\DeclareOption{letterpaper}
   {\setlength\paperheight {11in}%
    \setlength\paperwidth  {8.5in}}
\DeclareOption{legalpaper}
   {\setlength\paperheight {14in}%
    \setlength\paperwidth  {8.5in}}
\DeclareOption{executivepaper}
   {\setlength\paperheight {10.5in}%
    \setlength\paperwidth  {7.25in}}
\DeclareOption{landscape}
   {\setlength\@tempdima   {\paperheight}%
    \setlength\paperheight {\paperwidth}%
    \setlength\paperwidth  {\@tempdima}}

\DeclareOption{10pt}{\renewcommand\@ptsize{0}}
\DeclareOption{11pt}{\renewcommand\@ptsize{1}}
\DeclareOption{12pt}{\renewcommand\@ptsize{2}}

\DeclareOption{oneside}{\@twosidefalse \@mparswitchfalse}
\DeclareOption{twoside}{\@twosidetrue  \@mparswitchtrue}

\DeclareOption{draft}{\setlength\overfullrule{5pt}}
\DeclareOption{final}{\setlength\overfullrule{0pt}}

\DeclareOption{onecolumn}{\@twocolumnfalse}
\DeclareOption{twocolumn}{\@twocolumntrue}

\DeclareOption{leqno}{\input{leqno.clo}}
\DeclareOption{fleqn}{\input{fleqn.clo}}

\DeclareOption{openbib}{%
  \AtEndOfPackage{%
   \renewcommand\@openbib@code{%
      \advance\leftmargin\bibindent
      \itemindent -\bibindent
      \listparindent \itemindent
      \parsep \z@
      }%
   \renewcommand\newblock{\par}}%
}

\ExecuteOptions{a4paper,11pt,oneside,onecolumn,final}

\ProcessOptions

\input{size1\@ptsize.clo}
\setlength\lineskip{1\p@}
\setlength\normallineskip{1\p@}
\renewcommand\baselinestretch{}
\setlength\parskip{0\p@ \@plus \p@}
\@lowpenalty   51
\@medpenalty  151
\@highpenalty 301

%% We set these numbers slightly higher than in article, because
%% we rather want less pages in any case.
\setcounter{topnumber}{2}
\renewcommand\topfraction{.7}
\setcounter{bottomnumber}{2}
\renewcommand\bottomfraction{.4}
\setcounter{totalnumber}{4}
\renewcommand\textfraction{.1}
\renewcommand\floatpagefraction{.6}
\setcounter{dbltopnumber}{2}
\renewcommand\dbltopfraction{.7}
\renewcommand\dblfloatpagefraction{.6}

%% 6.4 Pagestyle (omitted, only myheadings exists)
\def\ps@myheadings{%
    \let\@oddfoot\@empty\let\@evenfoot\@empty
    \def\@evenhead{\thepage\hfil\slshape\leftmark}%
    \def\@oddhead{{\slshape\rightmark}\hfil\thepage}%
    \let\@mkboth\@gobbletwo
    \let\sectionmark\@gobble
    \let\subsectionmark\@gobble
    }
%% 7 Document Mark-up

%% 7.1 The title ------------------------------------------------------
%% Here it gets interesting.  We want \title (in center), 
%% \lefttitle and \righttitle for upper left and right as well as
%% \lowerright (right side, just below the title)

\global\let\thanks\relax % No \thanks, \author, \date, \and command!
\global\let\@thanks\@empty 
\global\let\@author\@empty
\global\let\author\relax
\global\let\date\relax
\global\let\@date\@empty
\global\let\and\relax

%% Instead, we have these commands
\def\@lefttitle{Use \texttt{$\backslash$lefttitle$\{$Text$\}$}}
\def\@righttitle{Use \texttt{$\backslash$righttitle$\{$Text$\}$}}
\def\@lowerright{Use \texttt{$\backslash$lowerright$\{$Text$\}$}}
\def\@title{Use \texttt{$\backslash$title$\{$Text$\}$}}
\def\lefttitle#1{\gdef\@lefttitle{#1}}
\def\righttitle#1{\gdef\@righttitle{#1}}
\def\lowerright#1{\gdef\@lowerright{#1}}

\newcommand\maketitle{\par
  \begingroup
    \if@twocolumn
      \ifnum \col@number=\@ne
        \@maketitle
      \else
        \twocolumn[\@maketitle]%
      \fi
    \else
      \newpage
      \@maketitle
    \fi
    \global\@topnum\z@   % Prevents figures from going at top of page.
  \endgroup
  \global\let\maketitle\relax
  \global\let\@maketitle\relax
  \global\let\@title\@empty
  \global\let\title\relax
}

\def\@maketitle{%
  \null
  \hbox to \linewidth{%
    \rlap{\parbox[t]{\linewidth}{%
        \@lefttitle\strut%
    }%
  }\hfill%
  \llap{\parbox[t]{\linewidth}{\raggedleft%
      \@righttitle\strut%
  }}}%
  \vskip 3ex%
  {\parbox[t]{\linewidth}{\centering\LARGE\bfseries \@title}}%
  \vskip0ex%
  \hfill%
  \llap{\parbox[t]{\linewidth}{\raggedleft%
    \@lowerright%
  }}%
  \vskip2ex
}
%% 7.2 -----------------------------------------------------------------
%% ltsect.dtx defines \@seccntformat differently (with an additional \quad
%% at the end).  We remove the quad, to get useful stuff for us.
%% This means that we may have to add a quad in \thetask and similar
%% things.
%%\def\@seccntformat#1{\csname the#1\endcsname}
\parindent=0pt
\setlength\parskip{0.5ex plus 0.1ex minus 0.05ex\relax}

\setcounter{secnumdepth}{1}
\newcounter{task}
\renewcommand\thetask{\@arabic\c@exercise.\@arabic\c@task\relax}
\let\taskmark\@gobble  %% No entry in the toc (yet) XXX

\newcommand\task{\par %% Needed to finish paragraph for next statement
                      %% not to mess up old paragraph
  \outofsubt@sk%
  \c@subtask=0\@startsection{task}{1}{0ex}%
  {-3.5ex \@plus -1ex \@minus -.2ex}%
  {0.3ex \@plus.2ex}%
  {\normalfont\bfseries}}

\newcounter{exercise}
\newif{\ifinsubt@sk}
\insubt@skfalse
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\newcounter{subtask}
\def\getintosubt@sk{
  \ifinsubt@sk\else%
       \global\advance\@listdepth\@ne%
       \global\advance\@enumdepth\@ne%
       \@listi
       \advance\linewidth -\rightmargin
       \advance\linewidth -\leftmargin
       \advance\@totalleftmargin \leftmargin
       \advance\leftskip\leftmargin
  \fi%
%  \parshape \@ne \@totalleftmargin \linewidth
  \global\insubt@sktrue%
}

\def\outofsubt@sk{
  \ifinsubt@sk%
       \global\advance\@listdepth\m@ne%
       \global\advance\@enumdepth\m@ne%
       \@listi
       \advance\linewidth\rightmargin
       \advance\linewidth\leftmargin
       \advance\@totalleftmargin-\leftmargin
       \advance\leftskip-\leftmargin
  \fi%
  \global\insubt@skfalse%
}
\newcommand*{\subtask}[1][]{\par\vskip0.5ex plus 0.2ex minus0.1ex%
             \getintosubt@sk%
             \advance\c@subtask by 1%
             {\noindent\llap{\hskip0.3em\bfseries\@alph\c@subtask)%
                             \hskip0.5em}}}
\def\nosubtask{\par\vskip0.5ex plus 0.2ex minus0.1ex%
               \outofsubt@sk}

\newcommand*{\subtaskTime}[1]{\subtask \textbf{(#1 Min)}}

%% 7.3 Lists -----------------------------------------------------------
%% We must define the labels in lists quite differently

%% Itemize / Description /enumerate
\if@twocolumn
  \setlength\leftmargini  {2em}
\else
  \setlength\leftmargini  {2.5em}
\fi
\leftmargin  \leftmargini
\setlength\leftmarginii  {2.2em}
\setlength\leftmarginiii {1.87em}
\setlength\leftmarginiv  {1.7em}
\if@twocolumn
  \setlength\leftmarginv  {.5em}
  \setlength\leftmarginvi {.5em}
\else
  \setlength\leftmarginv  {1em}
  \setlength\leftmarginvi {1em}
\fi
\setlength  \labelsep  {.5em}
\setlength  \labelwidth{\leftmargini}
\addtolength\labelwidth{-\labelsep}
\@beginparpenalty -\@lowpenalty
\@endparpenalty   -\@lowpenalty
\@itempenalty     -\@lowpenalty
\renewcommand\theenumi{\@alph\c@enumi}
\renewcommand\theenumii{\@roman\c@enumii}
\renewcommand\theenumiii{\@Alph\c@enumiii}
\newcommand\labelenumi{\textbf{\theenumi)}}
\newcommand\labelenumii{\theenumii.}
\newcommand\labelenumiii{\theenumiii.}
\renewcommand\p@enumii{\theenumi}
\renewcommand\p@enumiii{\theenumi(\theenumii)}
\renewcommand\p@enumiv{\p@enumiii\theenumiii}
\newcommand\labelitemi{\textbullet}
\newcommand\labelitemii{\normalfont\bfseries \textendash}
\newcommand\labelitemiii{\textasteriskcentered}
\newcommand\labelitemiv{\textperiodcentered}
\newenvironment{description}
               {\list{}{\labelwidth\z@ \itemindent-\leftmargin
                        \let\makelabel\descriptionlabel}}
               {\endlist}
\newcommand*\descriptionlabel[1]{\hspace\labelsep
                                \normalfont\bfseries #1}
%% 7.4 -----------------------------------------------------------------
% Abstract does not exist
% Verse does not exist
\newenvironment{quote}
               {\list{}{\rightmargin\leftmargin}%
                \item\relax}
               {\endlist}
% Thoerem does not exist
% Titlepage is not supported
% Forget about appendix

%% 7.5 Array, tabular, minipage, fbox, eqns ---------------------------
\setlength\arraycolsep{5\p@}
\setlength\tabcolsep{6\p@}
\setlength\arrayrulewidth{.4\p@}
\setlength\doublerulesep{2\p@}
\setlength\tabbingsep{\labelsep}
\skip\@mpfootins = \skip\footins
\setlength\fboxsep{3\p@}
\setlength\fboxrule{.4\p@}
\renewcommand \theequation {\@arabic\c@equation}
\newcounter{figure}
\renewcommand \thefigure {\@arabic\c@figure}
\def\fps@figure{tbp}
\def\ftype@figure{1}
\def\ext@figure{lof}
\def\fnum@figure{\figurename~\thefigure}
%% 7.6 Floating objects ------------------------------------------------
\newenvironment{figure}
               {\@float{figure}}
               {\end@float}
\newenvironment{figure*}
               {\@dblfloat{figure}}
               {\end@dblfloat}
\newcounter{table}
\renewcommand\thetable{\@arabic\c@table}
\def\fps@table{tbp}
\def\ftype@table{2}
\def\ext@table{lot}
\def\fnum@table{\tablename~\thetable}
\newenvironment{table}
               {\@float{table}}
               {\end@float}
\newenvironment{table*}
               {\@dblfloat{table}}
               {\end@dblfloat}
\newlength\abovecaptionskip
\newlength\belowcaptionskip
\setlength\abovecaptionskip{10\p@}
\setlength\belowcaptionskip{0\p@}
\long\def\@makecaption#1#2{%
  \vskip\abovecaptionskip
  \sbox\@tempboxa{#1: #2}%
  \ifdim \wd\@tempboxa >\hsize
    #1: #2\par
  \else
    \global \@minipagefalse
    \hb@xt@\hsize{\hfil\box\@tempboxa\hfil}%
  \fi
  \vskip\belowcaptionskip}
%% Old font style commands
\DeclareOldFontCommand{\rm}{\normalfont\rmfamily}{\mathrm}
\DeclareOldFontCommand{\sf}{\normalfont\sffamily}{\mathsf}
\DeclareOldFontCommand{\tt}{\normalfont\ttfamily}{\mathtt}
\DeclareOldFontCommand{\bf}{\normalfont\bfseries}{\mathbf}
\DeclareOldFontCommand{\it}{\normalfont\itshape}{\mathit}
\DeclareOldFontCommand{\sl}{\normalfont\slshape}{\@nomath\sl}
\DeclareOldFontCommand{\sc}{\normalfont\scshape}{\@nomath\sc}
\DeclareRobustCommand*\cal{\@fontswitch\relax\mathcal}
\DeclareRobustCommand*\mit{\@fontswitch\relax\mathnormal}
%%======================================================================
%% 8 Cross referencing skipped (since we don't need a TOC/index/etc)
%% (Except footnotes)
\renewcommand\footnoterule{%
  \kern-3\p@
  \hrule\@width.4\columnwidth
  \kern2.6\p@}
\newcommand\@makefntext[1]{%
    \parindent 1em%
    \noindent
    \hb@xt@1.8em{\hss\@makefnmark}#1}
%%======================================================================
\newcommand\figurename{Figure}
\newcommand\tablename{Table}

\pagestyle{empty}
\pagenumbering{arabic}
\def\today{\ifcase\month\or
  January\or February\or March\or April\or May\or June\or
  July\or August\or September\or October\or November\or December\fi
  \space\number\day, \number\year}
\setlength\columnsep{10\p@}
\setlength\columnseprule{0\p@}

\if@twoside
\else
  \raggedbottom
\fi
\onecolumn
\endinput
