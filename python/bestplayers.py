from datetime import datetime
import pytz
import logging
import logging.handlers
import os
import os.path
import re
import subprocess
import sys


css_styles = """<!DOCTYPE html>
<html lang="vi">

<head>
    <title>Các kỳ thủ đạt giải nhiều nhất</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Raleway">
    <link rel="stylesheet" href="https://thivualaytot.github.io/css/main.css">
    <link rel="stylesheet" href="https://thivualaytot.github.io/css/topwinner.css">
    <link rel="stylesheet" href="https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css">
    <link rel="icon" href="https://raw.githubusercontent.com/ThiVuaLayTot/ThiVuaLayTot.github.io/main/images/favicon.ico" type="image/x-icon">
</head>

<body>
    <header class="container">
    <div class="page-header">
        <div class="logo">
            <a hre="https://thivualaytot.github.io" title="Thí Vua Lấy Tốt"><img srcc="/images/favicon.ico" title="Thí Vua Lấy Tốt"></a>
        </div>
        <ul class="navbar-nav">
            <li>
                <a hre="https://thivualaytot.github.io" title="Trang chủ TVLT">Trang chủ</a>
            </li>
            <li>
                <a hre="https://thivualaytot.github.io/blog" title="Các thông báo/bài đăng quan trọng của TVLT">Thông báo/Tin tức</a>
            </li>
            <li>
                <a hre="https://thivualaytot.github.io/vlogs" title="Các Video quan trọng của TVLT">Vlogs</a>
            </li>
            <li>
                <div class="dropdown">
                    <a class="dropbtn" hre="https://thivualaytot.github.io/social" title="Social media links">Xã hội
                      <i class="vn bx-caret-down"></i>
                    </a>
                    <div class="dropdown-content">
                        <a hre="https://thivualaytot.github.io/social#social">Các tài khoản MXH của TungJohn</a>
                        <a hre="https://thivualaytot.github.io/social#chat">Các đoạn chat của Thí Vua Lấy Tốt</a>
                        <a hre="https://thivualaytot.github.io/social#group">Các nhóm/CLB/máy chủ của Thí Vua Lấy Tốt</a>
                    </div>
                </div>
            </li>
            <li>
                <div class="dropdown">
                    <a class="dropbtn" hre="https://thivualaytot.github.io/game" title="Các trò chơi đơn giản">MiniGames
                      <i class="vn bx-caret-down"></i>
                    </a>
                    <div class="dropdown-content">
                        <a hre="https://thivualaytot.github.io/game/caro">Cờ Caro 3x3</a>
                        <a hre="https://thivualaytot.github.io/game/chesspursuit">ChessPursuit</a>
                        <a hre="https://thivualaytot.github.io/game/sliding">Shogi Sliding-Puzzles</a>
                        <a hre="https://thivualaytot.github.io/game/2048">2048</a>
                    </div>
                </div>
            </li>
            <li>
                <div class="dropdown">
                    <a class="dropbtn, active" hre="https://thivualaytot.github.io/lists" title="Các danh sách/bảng quan trọng">Danh sách/Tài liệu
                      <i class="vn bx-caret-down"></i>
                    </a>
                    <div class="dropdown-content">
                        <a class="active" hre="https://thivualaytot.github.io/tournaments">Danh sách tổng hợp các giải đấu</a>
                        <a hre="https://thivualaytot.github.io/libot-leaderboard">Bảng xếp hạng các Bot trên Lichess</a>
                        <a hre="https://chess.com/clubs/forum/view/quy-dinh-co-ban-cua-clb-tungjohn-playing-chess">Danh sách các tài khoản vi phạm</a>
                    </div>
                </div>
            </li>
            <li>
                <div class="dropdown">
                    <a class="dropbtn" hre="https://thivualaytot.github.io/leaders" title="Ban cán sự của Thí Vua Lấy Tốt">Leaders
                      <i class="vn bx-caret-down"></i>
                    </a>
                    <div class="dropdown-content">
                        <a hre="https://thivualaytot.github.io/leaders#admins">Administrators/Các Quản trị viên</a>
                        <a hre="https://thivualaytot.github.io/leaders#mods">Moderators/Các điều hành viên</a>
                        <a hre="https://thivualaytot.github.io/leaders#sponsors">Các nhà tài trợ/hợp tác với giải</a>
                    </div>
                </div>
            </li>
        </ul>
        <div>
            <label class="mode">
                <input type="checkbox" id="darkModeToggle">
                <i id="moon" class="vn bxs-moon" title="Bật/Tắt chế độ tối"></i>
            </label>
        </div>
    </div>
    </header>
    <button onclick="topFunction()" id="myBtn"  title="Trở lại đầu trang này"><i id="back2top" class="vn bxs-to-top"></i></button>

"""

footer_style = """
<div class="footer">
    <div class="footer-container">
        <div>
            <h3><a hre="https://thivualaytot.github.io" title="Thí Vua Lấy Tốt Website">Thí Vua Lấy Tốt</a></h3>
            <p><a hre="https://thivualaytot.github.io/social" title="Social media links">Các trang mạng</a></p>
            <p><a hre="https://thivualaytot.github.io/blog" title="Các bài Blog quan trọng của TVLT">Các thông báo & tin tức</a></p>
            <p><a hre="https://thivualaytot.github.io/vlogs" title="Các Video quan trọng của TVLT">Các Vlog</a></p>
            <p><a hre="https://thivualaytot.github.io/game" title="Các trò chơi đơn giản">Các trò chơi đơn giản</a></p>
            <p><a hre="https://thivualaytot.github.io/lists" title="Các danh sách/bảng quan trọng">Danh sách/Tài liệu</a></p>
            <p><a hre="https://thivualaytot.github.io/leaders" title="Ban cán sự của TVLT">Ban cán sự của TVLT</a></p>
        </div>
        <div>
            <h3 align="center"><a hre="https://thivualaytot.github.io/social">Social meadia links</a></h3>
            <strong><a hre="https://thivualaytot.github.io/social#social">Các tài khoản MXH của TungJohn</a></strong>
            <div class="button">
                <a hre="https://youtube.com/channel/UCvNW1NAWWjblgrP6JQI4MbQ" target="_blank" title="Kênh Youtube của TungJohn"><i class="vn bxl-youtube"></i></a>
                <a hre="https://facebook.com/TungJohn2005" target="_blank" title="Trang Facebook của TungJohn"><i class="vn bxl-facebook"></i></a>
                <a hre="https://twitch.tv/tungjohnplayingchess" target="_blank" title="Kênh Twitch của TungJohn"><i class="vn bxl-twitch"></i></a>
                <a hre="https://tiktok.com/@tungjohn2005" target="_blank" title="Tài khoản Tiktok của TungJohn"><i class="vn bxl-tiktok"></i></a>
                <a hre="https://chess.com/member/tungjohn2005" target="_blank" title="Tài khoản Chess.com của TungJohn"><img srcc="https://images.chesscomfiles.com/uploads/v1/user/33.862d5ff1.160x160o.578dc76c0662.png"></a>
                <a hre="https://lichess.org/@/Tungjohn2005" target="_blank" title="Tài khoản Lichess của TungJohn"><img srcc="/images/lichesslogo.png"></a>
                <a hre="https://shopee.vn/tungjohn2005" target="_blank" title="Shop cờ vua của TungJohn trên Shopee"><i class="vn bxs-shopping-bag"></i></a>
            </div>
            <strong><a hre="https://thivualaytot.github.io/social#group">Các Nhóm, Câu Lạc Bộ, Máy Chủ Của Thí Vua Lấy Tốt</a></strong>
            <div class="button">
                <a hre="https://clubs.chess.com/GkQy" target="_blank"><img width="22" srcc="https://images.chesscomfiles.com/uploads/v1/user/33.862d5ff1.160x160o.578dc76c0662.png"></a>
                <a hre="https://lichess.org/team/thi-vua-lay-tot-tungjohn-playing-chess" target="_blank" title="Đội Thí Vua Lấy Tốt trên Lichess"><img width="22" srcc="/images/lichesslogo.png"></a>
                <a hre="https://facebook.com/groups/586909589413729" target="_blank" title="Nhóm Facebook của Thí Vua Lấy Tốt"><i class="vn bxl-facebook"></i></a>
                <a hre="https://discord.gg/WUhW5Cs9gB" target="_blank" title="Máy chủ Discord của Thí Vua Lấy Tốt"><i class="vn bxl-discord"></i></a>
            </div>
        </div>
        <div>
            <br><br>
            <p>Web được xây dựng bởi Quản trị viên <a hre="https://thivualaytot.github.io/leaders#admins" title="Các quản trị viên">Đinh Hoàng Việt</a>.</p>
            <p>Mã nguồn trên <a hre="https://github.com/ThiVuaLayTot/ThiVuaLayTot.github.io" title="Mã nguồn của web trên Github"><i class="vn bxl-github"></i></a></p>
        </div>
    </div>
</div>
    <script srcc="https://thivualaytot.github.io/js/main.js"></script>
</body>

</html>

"""

information = """
      <p>Nếu sau tên người dùng có: <span class="loader"></span> nghĩa là người chơi này có khả năng không được đạt giải hoặc đạt giải khác và đang chờ xác thực,<img class="verified" srcc="https://s3.vio.edu.vn/assets/img/wrong_icon_2.png"> là người chơi đã nhận phần thưởng nhưng sau đó đã xác nhận là gian lận.</p>
      <p>Và nếu tài khoản đó bị đóng do gian lận thì chuyển giải sang người đứng thứ hạng phía sau.</p>
"""

def generate_h1_tag(filename):
    title = os.path.splitext(filename)[0]
    tz_VI = pytz.timezone('Asia/Ho_Chi_Minh')
    datetime_VI = datetime.now(tz_VI)
    h1_tag = f"""    <h1 align="center">Các kỳ thủ đạt giải {title} nhiều nhất</h1>
    <h2 align="center">Bạn có thể xem danh sách các kỳ thủ đạt giải {title} <a hre="https://thivualaytot.github.io/tournaments/tournaments/{title}">Ở đây</a>.</h2>
    <p align="right"><i>Lần cuối cập nhật: {datetime_VI.hour}:{datetime_VI.minute}:{datetime_VI.second}, ngày {datetime_VI.day} tháng {datetime_VI.month} năm {datetime_VI.year}</i></p>"""
    return h1_tag

def markdown_table_to_html(markdown_table):
    chesscom = f'https://chess.com'
    lichess = f'https://lichess.org'
    unverified_icon = f'https://s3.vio.edu.vn/assets/img/wrong_icon_2.png'
    rows = markdown_table.strip().split('\n')
    html_table = '      <table class="styled-table">\n'
    for i, row in enumerate(rows):
        if '---|---|---' in row:
            continue

        tag = 'th' if i == 0 else 'td'
        cells = re.split(r'\s*\|\s*', row)

        if len(cells) == 1 and cells[0] == '':
            continue
        
        html_table += '         <tr>\n'
        for cell in cells:
            # Dành cho dòng đầu tiên
            if cell.endswith('Hạng'):
                text = cell[0:]
                cell_content = f'       <{tag} class="stt">{text}</{tag}>'
            elif cell.endswith('👑'):
                text = cell[0:]
                cell_content = f'       <{tag} class="winner">{text}</{tag}>'
            elif cell.endswith('Các lần đạt giải'):
                text = cell[0:]
                cell_content = f'       <{tag}>{text}</{tag}>'
            # Dành cho tài khoản trên Chess.com
            elif cell.startswith('? @'):
                username = cell[3:]
                cell_content = f'       <{tag}><a hre="{chesscom}/member/{username}" title="Xem tài khoản Chess.com của {username}" target="_blank">{username}</a> <span class="loader"></span></{tag}>'
            elif cell.startswith('! @'):
                username = cell[3:]
                cell_content = f'       <{tag}><a hre="{chesscom}/member/{username}" title="Xem tài khoản Chess.com của {username}" target="_blank">{username} <img class="verified" srcc="{unverified_icon}" title="Tài khoản gian lận"></a></{tag}>'
            elif cell.startswith('@'):
                username = cell[1:]
                cell_content = f'       <{tag}><a hre="{chesscom}/member/{username}" title="Xem tài khoản Chess.com của {username}" target="_blank">{username}</a></{tag}>'
            # Dành cho tài khoản trên Lichess
            elif cell.startswith('$'):
                username = cell[1:]
                cell_content = f'       <{tag}><a hre="{lichess}/@/{username}" title="Xem tài khoản Lichess của {username}" target="_blank">{username}</a></{tag}>'
            # Dành cho các ô/dòng còn lại
            else:
                cell_content = f'       <{tag}>{cell}</{tag}>'
            html_table += f'    {cell_content}\n'
        html_table += '         </tr>\n'
    html_table += '''   </table>
        <br><br><hr>
    '''
    return html_table

directories = ['tournaments/bestplayers']

for directory in directories:
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            with open(os.path.join(directory, filename), 'r') as md_file:
                h1_tag = generate_h1_tag(filename)
                markdown_table = md_file.read()
                html_table = markdown_table_to_html(markdown_table)
                styled_html_table = css_styles + h1_tag + information + html_table + footer_style
                html_filename = os.path.splitext(filename)[0] + '.html'
                with open(os.path.join(directory, html_filename), 'w') as html_file:
                    html_file.write(styled_html_table)
