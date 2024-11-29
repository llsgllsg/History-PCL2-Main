#!/bin/bash

# 获取最新的 10 个 Issue 编号和标题
issues=$(gh issue list --repo Hex-Dragon/PCL2 --limit 10 --json number,title --jq '.')

# 临时存储编号和标题的字符串
numbers=""
titles=""

# 提取 Issue 编号和标题
for i in $(seq 0 9); do
    # 拼接数据
    numbers+="$(echo "$issues" | jq -r ".[$i].number") "
    titles+="$(echo "$issues" | jq -r ".[$i].title") "
done

# 打印获取的 Issue 编号和标题
echo "获取的 Issue 编号：$numbers"
echo "获取的 Issue 标题：$titles"

# 将字符串拆分成数组
# 使用 `read` 命令将字符串分割成数组
read -r -a number <<< "$numbers"
read -r -a title <<< "$titles"

# 基于最新 Issue 编号创建文件路径
file_path="Issue.xaml"
previous_file_path="Issue.xaml"

# 删除旧的 Issue 文件（如果存在），删除的是第二新的 Issue
if [ -e "$previous_file_path" ]; then
    echo "删除旧的 XAML 文件: $previous_file_path"
    rm "$previous_file_path"
else
    echo "没有找到旧的 XAML 文件，构建后将Github提交推送"
fi

# 判断是否存在该文件
if [ -e "$file_path" ]; then
    echo "文件存在，无需更改"
else
    echo "文件不存在，正在更新"
    # 创建新 XAML 文件，填入对应的内容
    cat <<EOF > "$file_path"
<local:MyCard Margin="0,0,0,15">
    <StackPanel Margin="20,14">
        <Grid>
            <Grid.ColumnDefinitions>
                <ColumnDefinition Width="3*"/>
                <ColumnDefinition Width="1*"/>
            </Grid.ColumnDefinitions>
            <StackPanel Grid.Column="0">
                <TextBlock FontSize="16"><Bold>Issue快讯</Bold></TextBlock>
                <TextBlock FontSize="14">你可以查看实时Issue列表</TextBlock>
                <TextBlock FontSize="14">提交Issue前可以瞄眼,请避免重复提交</TextBlock>
            </StackPanel>
            <local:MyIconTextButton Grid.Column="1" HorizontalAlignment="Right" EventType="打开网页" LogoScale="1"
                Text="Issues" EventData="https://github.com/Hex-Dragon/PCL2/issues" ToolTip="提交一个PCL Issue 如果是Bug修复后可以获取活跃橙"
                Logo="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0z M1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0z"/>
        </Grid>
        <Line X1="0" X2="100" Stroke="{DynamicResource ColorBrush6}" StrokeThickness="1.5" Stretch="Fill" Margin="0,8"/>
        <TextBlock FontSize="16" Margin="13,0,0,0"><Bold>最新Issue [latest:10 5min reload]</Bold></TextBlock>
        <StackPanel>
            <Grid>
                <Grid.RowDefinitions>
                    <RowDefinition Height="45" />
                    <RowDefinition Height="45" />
                    <RowDefinition Height="45" />
                    <RowDefinition Height="45" />
                    <RowDefinition Height="45" />
                    <RowDefinition Height="45" />
                    <RowDefinition Height="45" />
                    <RowDefinition Height="45" />
                    <RowDefinition Height="45" />
                    <RowDefinition Height="45" />
                </Grid.RowDefinitions>
                <Grid.ColumnDefinitions>
                    <ColumnDefinition Width="400" />
                </Grid.ColumnDefinitions>
EOF

    # 动态填入 Issue 编号和标题
    for i in $(seq 0 9); do
        cat <<EOF >> "$file_path"
                <local:MyListItem Title="Issue#${number[$i]}" Margin="5,0,0,0" IsHitTestVisible="False" Info="${title[$i]}" Grid.Row="$i" Grid.Column="1"/>
EOF
    done

    cat <<EOF >> "$file_path"
            </Grid>
        </StackPanel>
    </StackPanel>
</local:MyCard>
EOF
fi


